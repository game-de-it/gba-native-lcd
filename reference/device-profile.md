# Target device profile

- Product: GT78-VN
- Android: 12
- Display: 960 x 640
- RetroArch: 1.22.2_GIT
- Video driver: gl
- OpenGL ES property: 196610 (OpenGL ES 3.2)
- CPU ABI: arm64-v8a
- Platform: MediaTek MT6785
- GBA native resolution: 240 x 160
- Integer relationship: exact 4x in both axes

## RetroArch state observed before shader work

- `video_shader_enable = true`
- `video_smooth = false`
- `video_scale_integer = false`
- Custom viewport: 960 x 640 at 0,0
- Shader directory in configuration: `/data/user/0/com.retroarch/shaders`

The app-private shader directory is not directly writable over normal ADB. Test
files should therefore be staged in shared storage and selected from RetroArch,
or copied into app-private storage by RetroArch itself.
