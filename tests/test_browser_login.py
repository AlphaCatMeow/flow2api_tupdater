import unittest
from unittest.mock import AsyncMock, patch

from token_updater.browser import BrowserManager


class BrowserLoginHelperTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.manager = BrowserManager()

    def test_detect_login_blocker_handles_two_factor_prompt(self):
        message = self.manager._detect_login_blocker("2-Step Verification\nCheck your phone")
        self.assertEqual(message, "该账号需要人工完成二次验证，请改用手动登录")

    async def test_auto_login_requires_credentials(self):
        profile = {
            "id": 1,
            "name": "alpha",
            "login_account": "",
            "login_password": "",
        }

        with patch("token_updater.browser.profile_db.get_profile", AsyncMock(return_value=profile)):
            result = await self.manager.auto_login(1)

        self.assertFalse(result["success"])
        self.assertIn("请先为该账号配置登录账号和登录密码", result["error"])


if __name__ == "__main__":
    unittest.main()
