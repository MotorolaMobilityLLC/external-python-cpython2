/*================================================================
** Copyright 2000, Clark Cooper
** All rights reserved.
**
** This is free software. You are permitted to copy, distribute, or modify
** it under the terms of the MIT/X license (contained in the COPYING file
** with this distribution.)
**
**
*/

#ifndef WINCONFIG_H
#define WINCONFIG_H

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#undef WIN32_LEAN_AND_MEAN

#include <memory.h>
#include <string.h>

#define XML_NS 1
#define XML_DTD 1
#define XML_BYTE_ORDER 12
#define XML_CONTEXT_BYTES 1024

#endif /* ndef WINCONFIG_H */
