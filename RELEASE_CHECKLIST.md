# v0.1.1 release checklist

- [x] Final `native-lcd-v0.1.1` shader files match the APK bootstrap assets
  byte-for-byte.
- [x] Legacy `native-lcd-v0.1.0` remains bundled and unchanged for comparison.
- [x] Default mGBA core preset references
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.1/`.
- [x] Shared shader browser root is
  `/storage/emulated/0/RetroArch/shaders/`.
- [x] English and Japanese documentation includes the final comparison images,
  shader paths, save paths, update behavior and KPA-only scope.
- [x] User completed final physical verification of the shader on KONKR Pocket
  ADVANCE before release preparation.
- [x] Rebuild the Arm64 APK with the final shader assets.
- [x] Sign with the persistent release certificate and verify its fingerprint.
- [x] Verify APK package name, version, ABI and embedded shader assets.
- [x] Build and test the bilingual shader-only ZIP.
- [x] Generate and verify `SHA256SUMS` for every release asset.
- [x] Commit and push the shader repository. The modified RetroArch source is
  published at `06cc964`.
- [x] Publish the bilingual GitHub v0.1.1 release and upload all assets.
- [x] Read back the public release metadata and asset checksums.
