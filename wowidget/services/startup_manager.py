import os
import subprocess
import sys
from pathlib import Path
from typing import Final

STARTUP_VALUE_NAME: Final[str] = "WoWidget"
RUN_KEY_PATH: Final[str] = r"Software\Microsoft\Windows\CurrentVersion\Run"


class StartupManager:
    def __init__(
        self,
        *,
        entry_script: Path | None = None,
    ) -> None:
        self.entry_script = (
            entry_script if entry_script is not None else self._detect_entry_script()
        )

    def is_supported(
        self,
    ) -> bool:
        return os.name == "nt"

    def is_enabled(
        self,
    ) -> bool:
        if not self.is_supported():
            return False

        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RUN_KEY_PATH,
                0,
                winreg.KEY_READ,
            ) as key:
                winreg.QueryValueEx(
                    key,
                    STARTUP_VALUE_NAME,
                )

                return True

        except FileNotFoundError:
            return False

        except OSError as error:
            raise RuntimeError("Unable to read the Windows startup setting.") from error

    def enable(
        self,
        *,
        start_minimized: bool,
    ) -> None:
        if not self.is_supported():
            raise RuntimeError("Launch with Windows is only supported " "on Windows.")

        import winreg

        command = self.build_startup_command(start_minimized=start_minimized)

        try:
            with winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER,
                RUN_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.SetValueEx(
                    key,
                    STARTUP_VALUE_NAME,
                    0,
                    winreg.REG_SZ,
                    command,
                )

        except OSError as error:
            raise RuntimeError("Unable to add WoWidget to Windows startup.") from error

    def disable(
        self,
    ) -> None:
        if not self.is_supported():
            return

        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RUN_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                try:
                    winreg.DeleteValue(
                        key,
                        STARTUP_VALUE_NAME,
                    )
                except FileNotFoundError:
                    pass

        except FileNotFoundError:
            pass

        except OSError as error:
            raise RuntimeError(
                "Unable to remove WoWidget from " "Windows startup."
            ) from error

    def set_enabled(
        self,
        enabled: bool,
        *,
        start_minimized: bool,
    ) -> None:
        if enabled:
            self.enable(start_minimized=start_minimized)
        else:
            self.disable()

    def build_startup_command(
        self,
        *,
        start_minimized: bool,
    ) -> str:
        arguments: list[str]

        if getattr(
            sys,
            "frozen",
            False,
        ):
            arguments = [str(Path(sys.executable).resolve())]

        else:
            python_executable = self._find_pythonw_executable()

            arguments = [
                str(python_executable),
                str(self.entry_script),
            ]

        if start_minimized:
            arguments.append("--minimized")

        return subprocess.list2cmdline(arguments)

    def reconcile(
        self,
        *,
        launch_with_windows: bool,
        start_minimized: bool,
    ) -> None:
        self.set_enabled(
            launch_with_windows,
            start_minimized=start_minimized,
        )

    @staticmethod
    def _detect_entry_script() -> Path:
        if getattr(
            sys,
            "frozen",
            False,
        ):
            return Path(sys.executable).resolve()

        return Path(sys.argv[0]).resolve()

    @staticmethod
    def _find_pythonw_executable() -> Path:
        executable = Path(sys.executable).resolve()

        if executable.name.lower() == "pythonw.exe":
            return executable

        candidate = executable.with_name("pythonw.exe")

        if candidate.is_file():
            return candidate

        return executable
