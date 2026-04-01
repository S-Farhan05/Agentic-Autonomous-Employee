import asyncio
from playwright.async_api import async_playwright
import sys
import os
from pathlib import Path

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

async def post_to_linkedin(content):
    """
    Post content to LinkedIn using Playwright automation
    """
    async with async_playwright() as p:
        print("🚀 Launching browser...")

        # Launch browser (visible so you can see what's happening)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Go to LinkedIn
            print("📱 Navigating to LinkedIn...")
            await page.goto('https://www.linkedin.com/login')

            print("\n⏳ Please log in to LinkedIn manually...")
            print("   Complete any 2FA/verification if needed...")
            print("   Script will continue when you reach the feed...\n")

            # Wait for navigation to feed (indicates successful login)
            print("⏳ Waiting for login to complete...")
            try:
                await page.wait_for_url('**/feed/**', timeout=120000)
                print("✅ Login successful!")
            except:
                # Check if we're already on LinkedIn (just not on feed)
                current_url = page.url
                if 'linkedin.com' in current_url and '/login' not in current_url:
                    print("⚠️  Already logged in, navigating to feed...")
                    try:
                        await page.goto('https://www.linkedin.com/feed/', timeout=30000)
                        await page.wait_for_timeout(3000)
                    except Exception as nav_error:
                        print(f"⚠️  Navigation issue: {nav_error}")
                        print("   Continuing anyway if on LinkedIn...")
                        if 'linkedin.com' not in page.url:
                            raise Exception("Not on LinkedIn after login attempt")
                else:
                    raise Exception("Login timeout - please try again")

            # Wait for page to fully load (skip networkidle as LinkedIn has continuous requests)
            print("⏳ Waiting for page to fully load...")
            await page.wait_for_timeout(5000)

            # Take screenshot for debugging
            try:
                screenshot_dir = Path(__file__).parent.parent / "debug"
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                screenshot_path = screenshot_dir / "linkedin_debug.png"
                await page.screenshot(path=str(screenshot_path), full_page=False)
                print(f"📸 Screenshot saved to: {screenshot_path}")
                print(f"   File size: {screenshot_path.stat().st_size} bytes")
            except Exception as screenshot_error:
                print(f"⚠️  Screenshot failed: {screenshot_error}")

            # Click "Start a post" button - try multiple approaches
            print("️  Clicking 'Start a post' button...")

            # First, close any open menus/popups (like the context menu shown in debug)
            print("🔍 Closing any open menus first...")
            try:
                await page.keyboard.press('Escape')
                await page.wait_for_timeout(500)
            except:
                pass

            clicked = False
            # Updated selectors based on LinkedIn's actual structure
            # The "Start a post" button is in a specific container, not just any button with "post"
            selectors_to_try = [
                # Most specific: the main "Start a post" button in the feed composer area
                ('div.share-box-feed-entry__trigger[role="button"]', 'share-box trigger div'),
                ('button.share-box-feed-entry__trigger', 'share-box trigger button'),
                # Alternative: button with specific aria-label
                ('button[aria-label="Start a post"]', 'exact aria-label'),
                # Fallback: text-based selectors (more reliable)
                ('button:has-text("Start a post")', 'text Start a post'),
                ('[role="button"]:has-text("Start a post")', 'role button with text'),
                # Last resort: the container div that acts as button
                ('.share-box-feed-entry__trigger', 'share-box class only'),
            ]

            for selector, desc in selectors_to_try:
                try:
                    # Wait for selector with longer timeout
                    element = await page.wait_for_selector(selector, timeout=5000, state='visible')
                    # Scroll into view first
                    await element.scroll_into_view_if_needed()
                    await page.wait_for_timeout(300)
                    # Click with force option
                    await element.click(force=True)
                    clicked = True
                    print(f"✅ Clicked using: {desc}")
                    break
                except Exception as e:
                    print(f"   Tried {desc}: {str(e)[:60]}")
                    continue

            if not clicked:
                # Last resort: try clicking by coordinates if we can find the element
                print("⚠️  Trying coordinate-based click...")
                try:
                    # Find the element and click it
                    start_post = await page.query_selector('.share-box-feed-entry__trigger')
                    if start_post:
                        box = await start_post.bounding_box()
                        if box:
                            await page.mouse.click(
                                box['x'] + box['width'] / 2,
                                box['y'] + box['height'] / 2
                            )
                            clicked = True
                            print("✅ Clicked using: coordinate-based click")
                except Exception as e:
                    print(f"   Coordinate click failed: {str(e)[:60]}")

            if not clicked:
                raise Exception("Could not find 'Start a post' button with any selector")

            # Wait for modal to open - scope to modal container
            print("⏳ Waiting for post editor modal to open...")
            await page.wait_for_timeout(5000)

            # Take screenshot after clicking to debug
            try:
                screenshot_path2 = screenshot_dir / "linkedin_modal_debug.png"
                await page.screenshot(path=str(screenshot_path2), full_page=False)
                print(f"📸 Modal screenshot saved to: {screenshot_path2}")
                print(f"   File size: {screenshot_path2.stat().st_size} bytes")
            except Exception as screenshot_error2:
                print(f"⚠️  Modal screenshot failed: {screenshot_error2}")

            # Close any lingering menus first
            try:
                await page.keyboard.press('Escape')
                await page.wait_for_timeout(500)
            except:
                pass

            # Wait for the modal dialog to appear - try multiple selectors
            modal_selectors = [
                'div[role="dialog"][aria-labelledby]',
                'div[role="dialog"]',
                '.share-creation-state',
                '.artdeco-modal',
                'div.share-box-feed-entry__container',
                '[data-test-modal]',
                '.ip-rte',  # Rich text editor container
            ]

            modal = None
            for selector in modal_selectors:
                try:
                    modal_element = await page.wait_for_selector(selector, timeout=3000, state='visible')
                    modal = modal_element
                    print(f"✅ Modal found using: {selector}")
                    break
                except Exception as e:
                    print(f"   Tried {selector}: {str(e)[:50]}")
                    continue

            if not modal:
                # Try to find any visible contenteditable area
                print("⚠️  Trying to find any visible contenteditable area...")
                try:
                    editor_area = await page.wait_for_selector('[contenteditable="true"]', timeout=3000, state='visible')
                    print("✅ Found contenteditable area, proceeding without modal scope")
                    modal = page  # Use page as fallback
                except:
                    # Check if we're already in a post creation page/view
                    print("⚠️  Checking if already in post creation view...")
                    current_url = page.url
                    if 'linkedin.com' in current_url:
                        print("   On LinkedIn, trying direct editor search...")
                        modal = page  # Use page as fallback
                    else:
                        raise Exception("Could not find post creation modal or editor")

            await page.wait_for_timeout(1000)

            # Type the content - SCOPED TO MODAL
            print("📝 Typing post content...")

            # Try multiple editor selectors within the modal
            typed = False
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                '[contenteditable="true"]',
                'div[role="textbox"]',
                '.ql-editor',
                '.ip-rte',  # LinkedIn's rich text editor
                'div[aria-label*="post"]',  # Post text area
            ]

            for selector in editor_selectors:
                try:
                    editor = modal.locator(selector).first if hasattr(modal, 'locator') else page.locator(selector).first
                    await editor.wait_for(timeout=5000)
                    await editor.click()
                    await page.wait_for_timeout(500)
                    # Clear any existing text first
                    await page.keyboard.press('Control+a')
                    await page.wait_for_timeout(200)
                    await page.keyboard.press('Delete')
                    await page.wait_for_timeout(200)
                    # Type the content
                    await editor.type(content, delay=30)
                    typed = True
                    print(f"✅ Content typed using: {selector}")
                    break
                except Exception as e:
                    print(f"   Tried editor {selector}: {str(e)[:50]}")
                    continue

            if not typed:
                # Fallback: use keyboard to type directly
                print("⚠️  Using fallback: direct keyboard input...")
                try:
                    await page.keyboard.type(content, delay=30)
                    typed = True
                    print("✅ Content typed using: direct keyboard input")
                except Exception as e:
                    raise Exception(f"Could not find text editor in modal: {e}")

            await page.wait_for_timeout(1000)

            # Click Post button - SCOPED TO MODAL
            print("📤 Publishing post...")

            # Try multiple Post button selectors within the modal
            posted = False
            post_selectors = [
                'button.share-actions__primary-action:not([disabled])',
                'button[aria-label*="Post"]:not([disabled])',
                'button:has-text("Post"):not([disabled])',
                '.share-actions__primary-action',
            ]

            for selector in post_selectors:
                try:
                    post_button = modal.locator(selector).first
                    await post_button.wait_for(timeout=5000)
                    await post_button.click()
                    posted = True
                    print(f"✅ Clicked Post button using: {selector}")
                    break
                except:
                    continue

            if not posted:
                raise Exception("Could not find Post button in modal")

            # Wait for post to be published
            print("⏳ Waiting for post to publish...")
            await page.wait_for_timeout(5000)

            # Take success screenshot
            try:
                success_screenshot = screenshot_dir / "linkedin_post_success.png"
                await page.screenshot(path=str(success_screenshot), full_page=False)
                print(f"📸 Success screenshot saved to: {success_screenshot}")
                print(f"   File size: {success_screenshot.stat().st_size} bytes")
            except Exception as success_error:
                print(f"⚠️  Success screenshot failed: {success_error}")

            print("\n✅ Post published successfully!")
            print("🔗 Check your LinkedIn feed to verify\n")
            print(f"📁 All screenshots saved in: {screenshot_dir}\n")

            # Log the action
            log_post_action(content, "success")

        except Exception as e:
            print(f"\n❌ Error posting: {e}\n")
            log_post_action(content, "failed", str(e))

        finally:
            print("🔒 Closing browser...")
            await browser.close()

def log_post_action(content, status, error=None):
    """Log the posting action to vault logs"""
    from datetime import datetime
    import json

    vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
    log_file = vault_path / "Logs" / "linkedin_posts.log"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "linkedin_post",
        "status": status,
        "content_preview": content[:100] + "..." if len(content) > 100 else content,
        "error": error
    }

    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linkedin_poster.py <post_content_or_file>")
        print("\nExample:")
        print('  python linkedin_poster.py "Your post content here"')
        print("\nOr read from file:")
        print('  python linkedin_poster.py linkedin_post_content.txt')
        sys.exit(1)

    content_arg = sys.argv[1]

    # Check if it's a file path
    content_path = Path(content_arg)
    if content_path.exists() and content_path.is_file():
        print(f"Reading content from file: {content_path}")
        content = content_path.read_text(encoding='utf-8')
    else:
        content = content_arg

    print("=" * 60)
    print("LinkedIn Automatic Poster")
    print("=" * 60)
    print(f"\nPost content ({len(content)} characters):")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()

    asyncio.run(post_to_linkedin(content))
