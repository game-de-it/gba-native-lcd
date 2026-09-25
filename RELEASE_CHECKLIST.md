# v0.1.0 release checklist

- [x] Shader files in the APK match `variants/` byte-for-byte.
- [x] English and Japanese README files include screenshots and save paths.
- [x] Final development build verified on KONKR Pocket ADVANCE / GT78-VN.
- [x] APK checksum generated in `dist/v0.1.0/SHA256SUMS`.
- [x] RetroArch modifications committed from base `d048deca5c11d6c66321099c1bdd37c02cba2098`.
- [ ] Choose and document a redistribution license for project-authored shader,
  documentation and photographs.
- [ ] Create and securely back up a persistent Android release keystore.
- [ ] Rebuild and sign the APK with that release key.
- [ ] Verify an in-place update using two consecutively signed test versions.
- [ ] Publish the modified RetroArch source commit and link it from the release.
- [ ] Upload the signed APK and matching checksum to the GitHub release.
