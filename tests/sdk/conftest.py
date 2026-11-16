"""Pin official GenVM runner for the older official Direct Mode loader.

genlayer-test 0.29.2 has no GENVM_VERSION env support; the default release
resolver selects v0.3.0-rc7 but that release renamed genvm-universal.tar.xz.
This version pin changes only the runner bundle, never mocked contract results.
"""
import gltest.direct.sdk_loader as sdk_loader
sdk_loader.get_latest_version = lambda: "v0.2.16"
