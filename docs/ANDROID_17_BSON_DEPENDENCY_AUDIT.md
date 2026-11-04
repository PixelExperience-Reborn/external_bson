# P2 — historical external/bson: PixelExperience-Reborn AOSP 17

**Audited:** 2026-11-04. **Verdict:** do not activate this archived module in the staged AOSP17 source manifest without a proven native or vendor consumer. This is a **dependency audit**, not a permanent decision to remove BSON support.

## Provenance and actual module boundary

- Repository: `PixelExperience-Reborn/external_bson`, historical `seventeen` SHA `ec09ff2859b4f2b1d5591b2e595d3b586c391f59` (commit dated 2018). The same HEAD was found on historical `eleven`, `twelve`, `thirteen`, and `fourteen`.
- The original [README](../README) calls this an early/alpha MongoDB C driver; core source is 2009–2010 code, with Apache-2.0 copyright notices.
- Root `Android.bp` uses `subdirs = ["*"]`. The actual [`src/Android.bp`](../src/Android.bp) exports one `cc_library_shared` called **`libbson`**, `vendor_available: true`, and builds only **`bson.c`** and **`numbers.c`** with `-DMONGO_HAVE_STDINT`. The networking driver `mongo.c` is **not** part of that Android module. Other source files remain in the archive.
- In the original PE `snippets/pixel-extras.xml`, project path is `external/bson`. The staged `aosp17_pe_p1_timezonepicker.xml` does **not** add it, and `aosp17_reference.xml` does not declare this historical project.
- A preliminary org-scoped GitHub code search returned no `libbson` results, but code indexing can be incomplete. **Do not conclude no consumers exist** without checking the complete synced product's Soong module graph, source dependencies, binary DT_NEEDED/Symbol references and vendor availability.

## Android17 decision

1. Keep the old PE BSON C implementation **archived and unselected** from staged base-only manifests. No automatic `external/bson` checkout, Soong namespace, `PRODUCT_PACKAGES += libbson`, or vendor image packaging.
2. If a real product/build or proprietary HAL requires `libbson`, identify its exact module/ELF consumer, partition, source provenance and ABI before reintroduction. Compare current maintained libraries rather than reviving this early driver by default.
3. Reassess the historical `subdirs` declaration, `vendor_available`, header exports, C99/Android17 Clang warnings, sanitizers, licenses, security parsing and partition policy with a full AOSP17 Soong build.
4. Any eventual modernization must preserve the BSON data contract and be tested with malformed inputs and its real users. The host-only smoke test below **does not validate parser safety** or vendor use.

## Checks

- `tools/verify_a17_bson_archive.py` verifies the archived Android.bp module/source selection and root assumptions.
- `.github/workflows/a17-bson-archive-audit.yml` additionally runs a host C99 shared-library compilation and a minimal trusted `bson_empty` / `bson_size` smoke test. This can establish **host compile compatibility only**; no Android17 Soong/Clang, sanitizer fuzzing, APK, full OTA or mondrian runtime is claimed.

**Integration status:** P2 source review complete after host CI; retain future need-to-port question open if a consumer emerges. No change to the historical `seventeen` branch.
