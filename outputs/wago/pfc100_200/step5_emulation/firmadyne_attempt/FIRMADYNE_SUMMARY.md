# Firmadyne Full-System Emulation Attempt: WAGO PFC100/200

This folder records a Firmadyne-style full-system emulation attempt for the WAGO PFC100/200 firmware.

## Completed Steps

- Firmadyne environment configured
- PostgreSQL database initialized
- Extractor dependencies installed
- WAGO firmware registered as image ID 1
- Existing extracted root filesystem packaged as Firmadyne image tarball
- Architecture detected as ARM little-endian (`armel`)
- QEMU disk image created using `makeImage.sh`
- Network inference attempted using `inferNetwork.sh`
- Firmadyne generated `scratch/1/run.sh`
- Full-system QEMU emulation script executed with timeout

## Key Results

- `images/1.tar.gz` was created manually from the extracted WAGO root filesystem.
- `scratch/1/image.raw` was generated successfully.
- `scratch/1/qemu.initial.serial.log` was generated.
- `scratch/1/run.sh` was generated and executed.
- Runtime boot activity was observed in the serial log.
- Network inference completed but did not identify reachable interfaces.

## Current Limitation

Firmadyne reported `Interfaces: []` during network inference. The serial log also showed that `/firmadyne/libnvram.so` could not be preloaded. This suggests that the firmware reaches runtime execution, but full reachable networking is not yet available through the current Firmadyne configuration.

## Interpretation

This completes the first Firmadyne-style full-system emulation attempt for the WAGO firmware. The workflow successfully produced a QEMU disk image, boot log, and runnable emulation script. The next step is to debug network/NVRAM behavior or compare this result with FirmAE.
