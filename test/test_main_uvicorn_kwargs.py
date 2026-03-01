import main
import unittest
from unittest.mock import patch


class BuildUvicornKwargsTests(unittest.TestCase):
    def test_darwin_with_uvloop_and_httptools_sets_runtime_options(self):
        with patch.object(main.platform, "system", return_value="Darwin"), patch.object(
            main.importlib.util,
            "find_spec",
            side_effect=lambda name: object() if name in {"uvloop", "httptools"} else None,
        ):
            kwargs = main.build_uvicorn_kwargs("0.0.0.0", 3214, "INFO")

        self.assertEqual(kwargs["host"], "0.0.0.0")
        self.assertEqual(kwargs["port"], 3214)
        self.assertEqual(kwargs["log_level"], "info")
        self.assertEqual(kwargs["loop"], "uvloop")
        self.assertEqual(kwargs["http"], "httptools")

    def test_darwin_without_uvloop_and_httptools_omits_runtime_options(self):
        with patch.object(main.platform, "system", return_value="Darwin"), patch.object(
            main.importlib.util, "find_spec", return_value=None
        ):
            kwargs = main.build_uvicorn_kwargs("127.0.0.1", 8000, "DEBUG")

        self.assertEqual(kwargs["host"], "127.0.0.1")
        self.assertEqual(kwargs["port"], 8000)
        self.assertEqual(kwargs["log_level"], "debug")
        self.assertNotIn("loop", kwargs)
        self.assertNotIn("http", kwargs)

    def test_non_darwin_omits_runtime_options_even_when_packages_exist(self):
        with patch.object(main.platform, "system", return_value="Linux"), patch.object(
            main.importlib.util, "find_spec", return_value=object()
        ):
            kwargs = main.build_uvicorn_kwargs("localhost", 9000, "WARNING")

        self.assertEqual(kwargs["host"], "localhost")
        self.assertEqual(kwargs["port"], 9000)
        self.assertEqual(kwargs["log_level"], "warning")
        self.assertNotIn("loop", kwargs)
        self.assertNotIn("http", kwargs)


if __name__ == "__main__":
    unittest.main()
