# FirmAE Attempt: WAGO PFC100/200

FirmAE was installed and initialized successfully on the Ubuntu host. The WAGO PFC100/200 firmware was submitted to FirmAE check mode.

## Result

FirmAE successfully started the workflow:

- Firmware extraction completed.
- Architecture detection completed.
- Emulation setup started.
- Image ID: 1.
- Mode: check.

## Failure Point

FirmAE failed during filesystem patching with the following errors:

```text
ln: /bin/sh: Not a directory
rm: can't stat '/sbin/reboot': Not a directory
cp: cannot stat '/home/fabiha/FirmAE/scratch/1/image//bin/a': Not a directory
Inspection showed that the extracted WAGO filesystem contains /bin, /sbin, and /lib as regular files rather than directories or symlinks. This breaks FirmAE's default patching assumptions.

Manual Investigation

The following layout was observed:

/bin  = regular file
/sbin = regular file
/lib  = regular file

A manual patch replacing them with symlinks to usr/bin, usr/sbin, and usr/lib succeeds locally, but rerunning FirmAE regenerates the scratch image and overwrites the manual patch.

Interpretation

FirmAE is installed and functional, but WAGO requires a filesystem-layout adaptation before FirmAE can proceed beyond patching. Compared with Firmadyne, FirmAE reaches extraction and architecture detection but currently fails earlier during rootfs patching due to WAGO-specific filesystem layout assumptions.
