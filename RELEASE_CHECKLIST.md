# v0.1.0 release checklist

- [x] Shader files in the APK match `variants/` byte-for-byte.
- [x] English and Japanese README files include screenshots and save paths.
- [x] Final release-signed build verified on KONKR Pocket ADVANCE (Android
  model: GT78-VN).
- [x] APK checksum generated in `dist/v0.1.0/SHA256SUMS`.
- [x] RetroArch modifications committed from base `d048deca5c11d6c66321099c1bdd37c02cba2098`.
- [x] License project-authored shader, tools and documentation under MIT while
  preserving RetroArch GPL-3.0+ and mGBA MPL-2.0 notices.
- [x] Create a persistent Android release keystore and record its public
  certificate fingerprint in `SIGNING_CERTIFICATE.md`.
- [x] Rebuild and sign the APK with that release key.
- [x] Verify release-key in-place reinstall while preserving `retroarch.cfg`,
  saves and states.
- [x] Verify GBA launch, shader rendering, accelerometer lighting and physical
  button input on the target device.
- [x] Publish the modified RetroArch source commit and link it from the release.
- [x] Upload the signed APK and matching checksum to the GitHub release.
