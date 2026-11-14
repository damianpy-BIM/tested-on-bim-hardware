// Copyright 2026 Cua AI, Inc.


// SPDX-License-Identifier: MIT
// Modified by BIM Groupe 14/11/2026: no Foundation/Metal link, lazy hook, quiet unless LUME_METAL_VERBOSE=1.

#import <objc/runtime.h>
#import <objc/message.h>
#include <mach-o/dyld.h>
#include <stdio.h>

#include <errno.h>
#include <stdlib.h>

typedef unsigned long long LumeU64;
typedef unsigned long NSUInteger;

typedef struct {
    BOOL enabled;
    NSUInteger appleFamilyMax;
    NSUInteger maxThreadgroupMemory;
    BOOL hasRecommendedWorkingSetSize;
    NSUInteger recommendedWorkingSetSize;
} LumeMetalConfiguration;

static LumeMetalConfiguration gConfiguration = {0};
static IMP gOriginalInitGPUFamilySupport = NULL;
static IMP gOriginalMaxThreadgroupMemoryLength = NULL;
static IMP gOriginalRecommendedMaxWorkingSetSize = NULL;
static IMP gOriginalSupportsFamily = NULL;
static BOOL gDeviceHooksInstalled = NO;

static BOOL parseUnsignedEnvironmentValue(const char *name, LumeU64 *value) {
    const char *rawValue = getenv(name);
    if (!rawValue || !*rawValue) return NO;

    errno = 0;
    char *end = NULL;
    unsigned long long parsed = strtoull(rawValue, &end, 0);
    if (errno != 0 || end == rawValue || !end || *end != '\0') return NO;

    *value = parsed;
    return YES;
}

static BOOL loadConfiguration(void) {
    LumeU64 appleFamilyMax = 0;
    if (!parseUnsignedEnvironmentValue(
            "LUME_METAL_APPLE_FAMILY_MAX",
            &appleFamilyMax
        ) || appleFamilyMax < 1001 || appleFamilyMax >= 2000) {
        return NO;
    }

    LumeU64 maxThreadgroupMemory = 65536;
    const char *rawThreadgroupMemory = getenv("LUME_METAL_MAX_THREADGROUP_MEMORY");
    if (rawThreadgroupMemory && *rawThreadgroupMemory &&
        !parseUnsignedEnvironmentValue("LUME_METAL_MAX_THREADGROUP_MEMORY", &maxThreadgroupMemory)) {
        return NO;
    }

    LumeU64 recommendedWorkingSetSize = 0;
    const char *rawWorkingSetSize = getenv("LUME_METAL_RECOMMENDED_WORKING_SET_SIZE");
    BOOL hasRecommendedWorkingSetSize = rawWorkingSetSize && *rawWorkingSetSize;
    if (hasRecommendedWorkingSetSize &&
        !parseUnsignedEnvironmentValue(
            "LUME_METAL_RECOMMENDED_WORKING_SET_SIZE",
            &recommendedWorkingSetSize
        )) {
        return NO;
    }

    gConfiguration.enabled = YES;
    gConfiguration.appleFamilyMax = (NSUInteger)appleFamilyMax;
    gConfiguration.maxThreadgroupMemory = (NSUInteger)maxThreadgroupMemory;
    gConfiguration.hasRecommendedWorkingSetSize = hasRecommendedWorkingSetSize;
    gConfiguration.recommendedWorkingSetSize = (NSUInteger)recommendedWorkingSetSize;
    return YES;
}

static NSUInteger hookMaxThreadgroupMemoryLength(id self, SEL selector) {
    NSUInteger original = gOriginalMaxThreadgroupMemoryLength
        ? ((NSUInteger(*)(id, SEL))(void *)gOriginalMaxThreadgroupMemoryLength)(self, selector)
        : 0;
    return original < gConfiguration.maxThreadgroupMemory
        ? gConfiguration.maxThreadgroupMemory
        : original;
}

static NSUInteger hookRecommendedMaxWorkingSetSize(id self, SEL selector) {
    NSUInteger original = gOriginalRecommendedMaxWorkingSetSize
        ? ((NSUInteger(*)(id, SEL))(void *)gOriginalRecommendedMaxWorkingSetSize)(self, selector)
        : 0;
    return original < gConfiguration.recommendedWorkingSetSize
        ? gConfiguration.recommendedWorkingSetSize
        : original;
}

static BOOL hookSupportsFamily(id self, SEL selector, NSUInteger family) {
    BOOL original = gOriginalSupportsFamily
        ? ((BOOL(*)(id, SEL, NSUInteger))(void *)gOriginalSupportsFamily)(self, selector, family)
        : NO;
    BOOL isConfiguredAppleFamily = family >= 1001 &&
        family <= gConfiguration.appleFamilyMax;
    return original || isConfiguredAppleFamily;
}

static BOOL replaceMethod(
    Class deviceClass,
    const char *selectorName,
    IMP replacement,
    IMP *original
) {
    SEL selector = sel_registerName(selectorName);
    Method method = class_getInstanceMethod(deviceClass, selector);
    if (!method) return NO;

    *original = method_setImplementation(method, replacement);
    return *original != NULL;
}

static void installDeviceHooks(id device) {
    @synchronized(object_getClass(device)) {
        if (gDeviceHooksInstalled) return;

        Class deviceClass = object_getClass(device);
        Method maxThreadgroupMemory = class_getInstanceMethod(
            deviceClass,
            sel_registerName("maxThreadgroupMemoryLength")
        );
        Method supportsFamily = class_getInstanceMethod(
            deviceClass,
            sel_registerName("supportsFamily:")
        );
        Method recommendedWorkingSetSize = gConfiguration.hasRecommendedWorkingSetSize
            ? class_getInstanceMethod(
                  deviceClass,
                  sel_registerName("recommendedMaxWorkingSetSize")
              )
            : NULL;

        if (!maxThreadgroupMemory || !supportsFamily ||
            (gConfiguration.hasRecommendedWorkingSetSize && !recommendedWorkingSetSize)) {
            if (getenv("LUME_METAL_VERBOSE")) fprintf(stderr, "[LumeMetalCapabilities] required device methods unavailable, stock capabilities kept\n");
            return;
        }

        BOOL installed = replaceMethod(
            deviceClass,
            "maxThreadgroupMemoryLength",
            (IMP)hookMaxThreadgroupMemoryLength,
            &gOriginalMaxThreadgroupMemoryLength
        );
        installed = installed && replaceMethod(
            deviceClass,
            "supportsFamily:",
            (IMP)hookSupportsFamily,
            &gOriginalSupportsFamily
        );

        if (installed && gConfiguration.hasRecommendedWorkingSetSize) {
            installed = replaceMethod(
                deviceClass,
                "recommendedMaxWorkingSetSize",
                (IMP)hookRecommendedMaxWorkingSetSize,
                &gOriginalRecommendedMaxWorkingSetSize
            );
        }

        if (!installed) {
            if (getenv("LUME_METAL_VERBOSE")) fprintf(stderr, "[LumeMetalCapabilities] hook installation incomplete\n");
            return;
        }

        gDeviceHooksInstalled = YES;
        if (getenv("LUME_METAL_VERBOSE")) fprintf(stderr, "[LumeMetalCapabilities] enabled (appleFamilyMax=%llu maxThreadgroupMemory=%llu)\n",
            (LumeU64)gConfiguration.appleFamilyMax, (LumeU64)gConfiguration.maxThreadgroupMemory);
    }
}

static void hookInitGPUFamilySupport(id self, SEL selector) {
    installDeviceHooks(self);
    ((void(*)(id, SEL))(void *)gOriginalInitGPUFamilySupport)(self, selector);
}

// BIM 14/11/2026: injected into every process by default, so nothing is loaded here. The hook is installed when an image
// that defines _MTLDevice (Metal) is added; processes that never load Metal pay one objc_getClass per loaded image.
static void installInitHook(void) {
    if (gOriginalInitGPUFamilySupport) return;
    Class deviceClass = objc_getClass("_MTLDevice");
    if (!deviceClass) return;
    Method method = class_getInstanceMethod(deviceClass, sel_registerName("initGPUFamilySupport"));
    if (!method) return;
    gOriginalInitGPUFamilySupport = method_setImplementation(method, (IMP)hookInitGPUFamilySupport);
}

static void onImageAdded(const struct mach_header *header, intptr_t slide) {
    (void)header; (void)slide;
    installInitHook();
}

__attribute__((constructor))
static void initializeLumeMetalCapabilities(void) {
    if (!loadConfiguration()) return;
    _dyld_register_func_for_add_image(onImageAdded);
}
