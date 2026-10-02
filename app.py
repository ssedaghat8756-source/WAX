# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template_string, abort, send_from_directory

app = Flask(__name__)

CREATOR_NAME = "سامان صداقت"
CREATOR_PHONE = "09300433442"
GAME_DOWNLOAD_URL = "https://edge-4-it.pgupgame.com/dl17/game/pc/Hollow.Knight/Hollow.Knight.1.5.78-ElAmigos-Par30Game.rar?1009236337"
APARAT_VIDEO = "https://www.aparat.com/video/video/embed/videohash/tqz7uav/vt/frame"
STORY_VIDEO = "https://www.aparat.com/video/video/embed/videohash/cve3yk1/vt/frame"


# ============================================================
# توابع کمکی برای کار با نام فایل‌ها
# ============================================================
def clean_filename(name):
    """نام فایل را پاک‌سازی می‌کند: lowercase + حذف پسوندهای تکراری."""
    name = name.lower().strip()
    exts = ['.jpeg', '.webp', '.jpg', '.png']
    changed = True
    while changed:
        changed = False
        for ext in exts:
            if name.endswith(ext):
                name = name[:-len(ext)]
                changed = True
                break
    return name


def is_image(filename):
    """بررسی می‌کند که آیا فایل یک تصویر است."""
    name = filename.lower()
    for ext in ['.jpeg', '.webp', '.jpg', '.png']:
        if name.endswith(ext):
            return True
    return False


def find_image(folder, target_id, variants=None):
    """در پوشه به دنبال فایل با نام پاک‌شده‌ی مطابق می‌گردد."""
    if not os.path.exists(folder):
        return None
    names_to_check = [target_id.lower()]
    if variants:
        names_to_check.extend([v.lower() for v in variants])
    try:
        files = os.listdir(folder)
    except OSError:
        return None
    for f in files:
        if not is_image(f):
            continue
        if clean_filename(f) in names_to_check:
            return f
    return None


def image_or_svg(folder, target_id, name_en, variants=None, size=200):
    """اگر عکس پیدا شد، img برمی‌گرداند؛ وگرنه SVG پیش‌فرض."""
    img_file = find_image(folder, target_id, variants)
    if img_file:
        return (
            f'<img src="/{folder}/{img_file}" alt="{name_en}" '
            f'style="max-width:100%;max-height:100%;object-fit:contain;">'
        )
    short_name = name_en[:15] if len(name_en) > 15 else name_en
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<circle cx="100" cy="100" r="90" fill="#1a1a25" stroke="#8a6a4a" stroke-width="2"/>
<text x="100" y="105" text-anchor="middle" fill="#8a6a4a" font-family="Arial" font-size="14" font-weight="bold">{short_name}</text>
</svg>'''


def boss_image_html(boss_id, name_en):
    variants_map = {
        "brothers_oro_mato": ["oro_mato", "brothers_oro_and_mato"],
        "the_hollow_knight": ["hollow_knight"],
        "grimm": ["troupe_master_grimm"],
        "radiance": ["the_radiance"],
    }
    return image_or_svg("images", boss_id, name_en, variants_map.get(boss_id))


def character_image_html(char_id, name_en):
    return image_or_svg("characters", char_id, name_en)


# ⬅️ جدید: تابع برای دریافت لیست تمام عکس‌های پوشه‌ی Knight
def get_knight_images():
    """تمام عکس‌های پوشه‌ی knight را برمی‌گرداند (مرتب‌شده)."""
    if not os.path.exists("knight"):
        return []
    files = [f for f in os.listdir("knight") if is_image(f)]
    # مرتب‌سازی بر اساس نام پاک‌شده
    files.sort(key=lambda x: clean_filename(x))
    return files


# ============================================================
# داستان بازی
# ============================================================
GAME_STORY = """
هالوونست (Hallownest) — پادشاهی ابدی حشرات — روزگاری سرزمینی پر رونق و باشکوه بود که توسط موجودی الهی به نام «پادشاه رنگ‌پریده» (The Pale King) اداره می‌شد. پادشاه رنگ‌پریده با نور خرد خود، حشرات را از توحش و غریزه رها کرد و به آن‌ها آگاهی و تمدن بخشید.

اما پیش از ظهور پادشاه، حشرات موجودی باستانی و نورانی به نام «رادیانس» (The Radiance) را می‌پرستیدند؛ خدای نور و خاطرات که در رؤیاها و ذهن‌ها حکومت می‌کرد.

هنگامی که پادشاه رنگ‌پریده قدرت را به دست گرفت و رادیانس به فراموشی سپرده شد، او خشمگین شد و برای انتقام، بیماری مرموزی به نام «عفونت» (The Infection) را در ذهن حشرات پخش کرد. عفونت، حشرات را به موجوداتی وحشی و دیوانه تبدیل می‌کرد و آرام آرام پادشاهی را به نابودی می‌کشاند.

پادشاه رنگ‌پریده برای نجات هالوونست، تصمیم گرفت رادیانس را درون موجودی زندانی کند. او با نیروی تاریک «وُید» (The Void) — جوهر نیستی و پوچی — موجوداتی بی‌احساس به نام «وسل» (Vessel) خلق کرد. این وسل‌ها قرار بود «توخالی» باشند تا بتوانند رادیانس را در خود زندانی کنند.

از میان هزاران وسل، یکی به نام «هالو نایت» (The Hollow Knight) برگزیده شد. پادشاه او را در معبد تخم سیاه (Temple of the Black Egg) زندانی کرد و سه موجود قدرتمند به نام «رویابین‌ها» (The Dreamers) — مونومون، لورین و هرا — با فدا کردن خود، معبد را مهروموم کردند.

اما هالو نایت یک نقص پنهان داشت: او نسبت به پدرش، پادشاه رنگ‌پریده، احساس عشق و دلبستگی داشت. همین احساس، باعث شد که عفونت رادیانس در او رخنه کند و به‌جای زندانی کردن رادیانس، خودش به زندان او تبدیل شود.

قرن‌ها بعد، هالوونست به ویرانه‌ای خاموش تبدیل شد. حشرات یا مرده‌اند، یا دیوانه، یا پنهان. اما شوالیه‌ای ناشناس — یکی از وسل‌های فراموش‌شده — به این سرزمین می‌آید. او بی‌نام، بی‌چهره و بی‌احساس است. سفری طولانی را آغاز می‌کند تا ریشه‌ی عفونت را نابود کند و هالوونست را آزاد سازد.

در طول سفر، شوالیه با دشمنان و متحدانی روبه‌رو می‌شود: هورنت، دختر پادشاه؛ رویابین‌ها؛ اربابان مانتیس؛ و در نهایت، خود هالو نایت. و در اعماق رؤیا، با رادیانس روبه‌رو می‌شود.

در پایان، شوالیه با اتحاد با وُید و تبدیل شدن به «خداوندگار وُید» (Void Given Focus)، رادیانس را برای همیشه نابود می‌کند و هالوونست را از نفرین عفونت آزاد می‌سازد.
"""

GAME_HISTORY = """
هالو نایت (Hollow Knight) یک بازی اکشن-ماجراجویی دوبعدی در سبک Metroidvania است که توسط استودیوی مستقل استرالیایی «تیم چری» (Team Cherry) ساخته و منتشر شده است.

📅 تاریخ انتشار: ۲۴ فوریه ۲۰۱۷ (نسخه‌ی PC)
🎮 پلتفرم‌ها: PC, Nintendo Switch, PlayStation 4, Xbox One
🏆 جوایز: نامزد بهترین بازی مستقل در جوایز BAFTA، برنده‌ی جوایز متعدد طراحی و موسیقی

📦 DLCها:
• Hidden Dreams (۲۰۱۷)
• The Grimm Troupe (۲۰۱۷)
• Lifeblood (۲۰۱۸)
• Godmaster (۲۰۱۸)

🎨 سبک: Metroidvania، اکشن-ماجراجویی
🎵 موسیقی: Christopher Larkin
👥 تیم سازنده: Ari Gibson و William Pellen
🎭 شخصیت اصلی: شوالیه‌ای ناشناس
🌍 داستان: کشف رازهای پادشاهی هالوونست و نابودی عفونت
"""


# ⬅️ جدید: بخش کامل شوالیه
KNIGHT_STORY = """
شوالیه (The Knight) — که با نام‌های Ghost of Hallownest و The Wanderer هم شناخته می‌شود — یکی از هزاران «وسل» (Vessel) است که توسط پادشاه رنگ‌پریده و بانوی سفید در «پرتگاه» (The Abyss) خلق شد.

پادشاه رنگ‌پریده برای زندانی کردن رادیانس، به موجودی نیاز داشت که «توخالی» (Hollow) باشد — بدون احساس، بدون اراده، بدون هیچ چیز. او با نیروی وُید (Void) هزاران وسل خلق کرد و آن‌ها را در Abyss رها کرد تا فقط یکی از آن‌ها که واقعاً «خالی» است، انتخاب شود.

از میان همه، «هالو نایت» (The Hollow Knight) به عنوان ظرف خالص انتخاب شد. اما شوالیه‌ی ما — که یکی از وسل‌های رهاشده بود — از پرتگاه بالا آمد و به Dirtmouth رسید.

او بی‌نام، بی‌چهره و بی‌احساس است. نه گذشته‌ای دارد و نه آینده‌ای. تنها هدفش، رسیدن به معبد تخم سیاه و نابودی عفونت است.

در طول سفر، شوالیه با موجودات مختلفی روبه‌رو می‌شود: هورنت، کویرل، کرنیفر، پیرحشره و... . او قدرتمندتر می‌شود، توانایی‌های جدید می‌آموزد و در نهایت با وُید یکی می‌شود تا رادیانس را برای همیشه نابود کند.

شوالیه نه قهرمان است و نه شرور. او فقط یک ظرف است که برای هدفی بزرگ خلق شده. و در سکوت، به سرنوشتش می‌رود.
"""

# ⬅️ جدید: توانایی‌ها و تجهیزات شوالیه
KNIGHT_ABILITIES = [
    {
        "name_fa": "میخ (Nail)",
        "name_en": "Nail",
        "icon": "⚔️",
        "desc": "سلاح اصلی شوالیه. با ارتقا در شهر اشک‌ها (City of Tears) می‌تواند از Old Nail به Sharpened Nail، Channeled Nail، Coiled Nail و در نهایت Pure Nail تبدیل شود. Pure Nail قوی‌ترین نسخه است.",
    },
    {
        "name_fa": "روح انتقام‌جو",
        "name_en": "Vengeful Spirit",
        "icon": "💥",
        "desc": "اولین طلسم شوالیه که در Forgotten Crossroads از Snail Shaman یاد می‌گیرد. یک روح آتشین به سمت دشمن پرتاب می‌کند.",
    },
    {
        "name_fa": "شیرجه‌ی متروک",
        "name_en": "Desolate Dive",
        "icon": "🌀",
        "desc": "شوالیه به زمین می‌کوبد و موجی از انرژی در اطرافش منتشر می‌کند. در Soul Sanctum به دست می‌آید.",
    },
    {
        "name_fa": "ارواح زوزه‌کش",
        "name_en": "Howling Wraiths",
        "icon": "👻",
        "desc": "سه روح از دهان شوالیه بیرون می‌آیند و به سمت بالا حمله می‌کنند. در Fog Canyon پیدا می‌شود.",
    },
    {
        "name_fa": "شنل پروانه",
        "name_en": "Mothwing Cloak",
        "icon": "🦋",
        "desc": "به شوالیه اجازه می‌دهد در هوا دَش (Dash) کند. بعد از شکست هورنت در Greenpath به دست می‌آید.",
    },
    {
        "name_fa": "پنجه‌ی مانتیس",
        "name_en": "Mantis Claw",
        "icon": "🦗",
        "desc": "به شوالیه اجازه می‌دهد از دیوارها بالا برود. در Mantis Village پیدا می‌شود.",
    },
    {
        "name_fa": "بال‌های پادشاه",
        "name_en": "Monarch Wings",
        "icon": "🦅",
        "desc": "به شوالیه اجازه‌ی پرش دوبل (Double Jump) می‌دهد. در Ancient Basin به دست می‌آید.",
    },
    {
        "name_fa": "قلب کریستال",
        "name_en": "Crystal Heart",
        "icon": "💎",
        "desc": "به شوالیه اجازه می‌دهد با سرعت زیاد در یک خط مستقیم پرواز کند. در Crystal Peak پیدا می‌شود.",
    },
    {
        "name_fa": "شمشیر رؤیا",
        "name_en": "Dream Nail",
        "icon": "🌙",
        "desc": "به شوالیه اجازه می‌دهد به ذهن موجودات وارد شود و رؤیاها را ببیند. در Resting Grounds به دست می‌آید.",
    },
    {
        "name_fa": "شنل سایه",
        "name_en": "Shade Cloak",
        "icon": "🌑",
        "desc": "نسخه‌ی ارتقایافته‌ی Mothwing Cloak که به شوالیه اجازه می‌دهد از دشمنان و موانع عبور کند. در The Abyss پیدا می‌شود.",
    },
    {
        "name_fa": "اشک ایزما",
        "name_en": "Isma's Tear",
        "icon": "💧",
        "desc": "به شوالیه اجازه می‌دهد در آب اسیدی شنا کند. در Royal Waterways پیدا می‌شود.",
    },
    {
        "name_fa": "نشان پادشاه",
        "name_en": "King's Brand",
        "icon": "👑",
        "desc": "نشان سلطنتی که در The Abyss پیدا می‌شود و به شوالیه اجازه‌ی ورود به White Palace را می‌دهد.",
    },
    {
        "name_fa": "قلب پوچ",
        "name_en": "Void Heart",
        "icon": "🖤",
        "desc": "قلب وُید که در انتهای بازی و پس از تکمیل مسیر به دست می‌آید. با آن، شوالیه می‌تواند رادیانس را برای همیشه نابود کند.",
    },
]

# ⬅️ جدید: مسیر سفر شوالیه
KNIGHT_JOURNEY = [
    {"region": "The Abyss", "region_fa": "پرتگاه", "icon": "🕳️", "desc": "تولد شوالیه از وُید. جایی که همه‌ی وسل‌ها رها شدند."},
    {"region": "Dirtmouth", "region_fa": "دهان خاک", "icon": "🌫️", "desc": "اولین جایی که شوالیه از پرتگاه بالا می‌آید و با Elderbug روبه‌رو می‌شود."},
    {"region": "Forgotten Crossroads", "region_fa": "گذرگاه فراموش‌شده", "icon": "🛤️", "desc": "اولین منطقه‌ی بازی. شوالیه اولین دشمنان را می‌بیند و False Knight را شکست می‌دهد."},
    {"region": "Greenpath", "region_fa": "مسیر سبز", "icon": "🌿", "desc": "جنگل سرسبز. شوالیه با Hornet روبه‌رو می‌شود و Mothwing Cloak را به دست می‌آورد."},
    {"region": "Fungal Wastes", "region_fa": "زباله‌های قارچی", "icon": "🍄", "desc": "قلمرو قارچ‌ها. شوالیه Mantis Claw را از Mantis Village می‌گیرد."},
    {"region": "City of Tears", "region_fa": "شهر اشک‌ها", "icon": "💧", "desc": "قلب هالوونست. شوالیه با Quirrel، Hornet و Watcher Knights روبه‌رو می‌شود."},
    {"region": "Crystal Peak", "region_fa": "قله‌ی کریستال", "icon": "💎", "desc": "قله‌ی درخشان. شوالیه Crystal Heart را به دست می‌آورد."},
    {"region": "Resting Grounds", "region_fa": "سرزمین آرامش", "icon": "🪦", "desc": "قبرستان مقدس. شوالیه Dream Nail را از Seer می‌گیرد."},
    {"region": "Deepnest", "region_fa": "تودرتوی عمیق", "icon": "🕷️", "desc": "قلمرو وحشت. شوالیه با Herrah و Nosk روبه‌رو می‌شود."},
    {"region": "The Abyss (بازگشت)", "region_fa": "بازگشت به پرتگاه", "icon": "🌑", "desc": "شوالیه با King's Brand به Abyss برمی‌گردد و Void Heart را به دست می‌آورد."},
    {"region": "Temple of the Black Egg", "region_fa": "معبد تخم سیاه", "icon": "🥚", "desc": "نبرد نهایی. شوالیه با The Hollow Knight و The Radiance مبارزه می‌کند."},
]

# ⬅️ جدید: پایان‌های بازی
KNIGHT_ENDINGS = [
    {
        "name_fa": "شوالیه‌ی توخالی",
        "name_en": "The Hollow Knight",
        "icon": "🥚",
        "desc": "پایان پایه. شوالیه The Hollow Knight را شکست می‌دهد و خودش در معبد زندانی می‌شود تا عفونت را در خود نگه دارد. چرخه‌ی رنج ادامه می‌یابد.",
        "requirement": "بدون Void Heart",
    },
    {
        "name_fa": "خواهران مهروموم",
        "name_en": "Sealed Siblings",
        "icon": "🔒",
        "desc": "هورنت به کمک شوالیه می‌آید و هر دو با هم در معبد مهروموم می‌شوند. باز هم چرخه ادامه می‌یابد.",
        "requirement": "بدون Void Heart + Hornet present",
    },
    {
        "name_fa": "دیگر رؤیایی نیست",
        "name_en": "Dream No More",
        "icon": "✨",
        "desc": "شوالیه با Void Heart وارد ذهن Hollow Knight می‌شود و رادیانس را برای همیشه نابود می‌کند. هالوونست آزاد می‌شود.",
        "requirement": "با Void Heart",
    },
    {
        "name_fa": "در آغوش کشیدن وُید",
        "name_en": "Embrace the Void",
        "icon": "🖤",
        "desc": "بهترین پایان. شوالیه در Godhome با Absolute Radiance مبارزه می‌کند و با وُید یکی می‌شود. رادیانس برای همیشه نابود می‌شود و شوالیه به خداوندگار وُید تبدیل می‌شود.",
        "requirement": "Void Heart + Pantheon of Hallownest",
    },
    {
        "name_fa": "گذر عصر",
        "name_en": "Passing of the Age",
        "icon": "🌸",
        "desc": "پایان ایستر اگ. شوالیه با Flower از Delicate Flower به سمت Hollow Knight می‌رود و او را به آرامش می‌رساند.",
        "requirement": "Delicate Flower",
    },
]

# ⬅️ جدید: چک‌لیست توانایی‌ها
KNIGHT_CHECKLIST = [
    "Mothwing Cloak", "Mantis Claw", "Monarch Wings", "Crystal Heart",
    "Dream Nail", "Shade Cloak", "Isma's Tear", "King's Brand", "Void Heart",
    "Vengeful Spirit", "Desolate Dive", "Howling Wraiths",
]


# ============================================================
# کاراکترها و مکان‌ها (صفحه‌ی تاریخ)
# ============================================================
CHARACTERS = [
    {
        "id": "temple_of_the_black_egg",
        "name_fa": "معبد تخم سیاه",
        "name_en": "Temple of the Black Egg",
        "type_fa": "مکان مقدس",
        "story_fa": """معبد تخم سیاه، قلب هالوونست و محل زندانی شدن رادیانس است. این معبد در نزدیکی Dirtmouth و بالای چاه ورودی قرار دارد. سه رویابین (Monomon, Lurien, Herrah) با فدا کردن خود، معبد را مهروموم کردند تا رادیانس برای همیشه زندانی بماند.

داخل معبد، هالو نایت (The Hollow Knight) زنجیر شده است. سه مهر جادویی روی در معبد وجود دارد که هر کدام مربوط به یک رویابین است. برای ورود به معبد و مبارزه با هالو نایت، شوالیه باید هر سه مهر را بشکند و Dream Nail را به دست آورد.

در پایان بازی، در اعماق معبد، شوالیه با هالو نایت و سپس رادیانس مبارزه می‌کند."""
    },
    {
        "id": "pale_king",
        "name_fa": "پادشاه رنگ‌پریده",
        "name_en": "The Pale King",
        "type_fa": "شخصیت اصلی",
        "story_fa": """پادشاه رنگ‌پریده، موجودی الهی و فرمانروای هالوونست است. او با نور خرد خود، حشرات را از غریزه رها کرد و به آن‌ها آگاهی و تمدن بخشید. اما پیش از ظهور او، حشرات رادیانس (The Radiance) را می‌پرستیدند.

وقتی رادیانس به فراموشی سپرده شد، او برای انتقام عفونت را پخش کرد. پادشاه برای نجات پادشاهی، با نیروی وُید موجوداتی به نام «وسل» خلق کرد و یکی از آن‌ها (The Hollow Knight) را برای زندانی کردن رادیانس برگزید.

پادشاه در نهایت خود را در کاخ سفید (White Palace) زندانی کرد و به دست فراموشی سپرده شد. اما روح او همچنان در رؤیاها زنده است."""
    },
    {
        "id": "white_lady",
        "name_fa": "بانوی سفید",
        "name_en": "The White Lady",
        "type_fa": "شخصیت اصلی",
        "story_fa": """بانوی سفید، ملکه‌ی هالوونست و همسر پادشاه رنگ‌پریده است. او موجودی الهی و مادر بسیاری از وسل‌هاست. بانوی سفید در باغ‌های ملکه (Queen's Gardens) سکونت دارد و درخت سفیدی است که ریشه‌هایش در سراسر هالوونست گسترده است.

او یکی از معدود موجوداتی است که از نقشه‌ی پادشاه برای زندانی کردن رادیانس آگاه است. بانوی سفید با فدا کردن فرزندانش (وسل‌ها) موافقت کرد، اما از این کار پشیمان است."""
    },
    {
        "id": "quirrel",
        "name_fa": "کویرل",
        "name_en": "Quirrel",
        "type_fa": "همراه و متحد",
        "story_fa": """کویرل، مسافری مرموز با کلاه‌خودی از جنس صدف است که در سراسر هالوونست با او روبه‌رو می‌شوی. او دوست و همراه شوالیه است و در مکان‌های مختلف به او کمک می‌کند.

کویرل در واقع شاگرد مونومون (Monomon the Teacher) بوده است. او برای یافتن استادش و شکستن مهر معبد تخم سیاه، به هالوونست آمده است. در نهایت، کویرل در آرشیوهای معلم (Teacher's Archives) با شوالیه روبه‌رو می‌شود و پس از کمک به او، کلاه‌خودش را درمی‌آورد و به آرامش می‌رسد."""
    },
    {
        "id": "cornifer",
        "name_fa": "کرنیفر",
        "name_en": "Cornifer",
        "type_fa": "همراه و متحد",
        "story_fa": """کرنیفر، نقشه‌کش و ماجراجوی هالوونست است. او در هر منطقه از بازی، در گوشه‌ای پنهان شده و در حال کشیدن نقشه است. وقتی شوالیه او را پیدا می‌کند، کرنیفر نقشه‌ی آن منطقه را به او می‌فروشد.

کرنیفر همسر ایزلدا (Iselda) است که در Dirtmouth یک مغازه‌ی نقشه‌فروشی دارد. او عاشق ماجراجویی و کشف مناطق جدید است و همیشه با لبخند و انرژی مثبت، شوالیه را راهنمایی می‌کند."""
    },
    {
        "id": "elderbug",
        "name_fa": "پیرحشره",
        "name_en": "Elderbug",
        "type_fa": "همراه و متحد",
        "story_fa": """پیرحشره، ساکن قدیمی Dirtmouth است که در ورودی چاه به هالوونست زندگی می‌کند. او تنها بازمانده‌ی Dirtmouth است که هنوز امید خود را از دست نداده است.

پیرحشره در ابتدای بازی، شوالیه را راهنمایی می‌کند و درباره‌ی پادشاهی هالوونست و عفونت برایش توضیح می‌دهد. او نگران سرنوشت هالوونست است و امیدوار است شوالیه بتواند پادشاهی را نجات دهد."""
    },
    {
        "id": "monomon",
        "name_fa": "مونومون معلم",
        "name_en": "Monomon the Teacher",
        "type_fa": "رویابین (Dreamer)",
        "story_fa": """مونومون، یکی از سه رویابین (Dreamers) است که با فدا کردن خود، معبد تخم سیاه را مهروموم کرد. او معلم و دانشمند بزرگ هالوونست بود و در آرشیوهای معلم (Teacher's Archives) در Fog Canyon سکونت داشت.

مونومون برای محافظت از دانش و کتاب‌هایش، موجودی به نام Uumuu را خلق کرد. او شاگردانی مثل کویرل داشت. وقتی شوالیه برای شکستن مهر معبد به سراغش می‌رود، مونومون در رؤیا زندانی است و شوالیه باید با Uumuu مبارزه کند تا به او برسد."""
    },
    {
        "id": "lurien",
        "name_fa": "لورین نگهبان",
        "name_en": "Lurien the Watcher",
        "type_fa": "رویابین (Dreamer)",
        "story_fa": """لورین، یکی از سه رویابین است که در برج نگهبان (Watcher's Spire) در شهر اشک‌ها سکونت داشت. او نگهبان شهر و مسئول نظارت بر امنیت هالوونست بود.

لورین برای محافظت از برج خود، شش شوالیه‌ی زره‌پوش به نام Watcher Knights را خلق کرد. او در بالای برج، در رؤیا زندانی است. شوالیه برای رسیدن به او، باید با Watcher Knights مبارزه کند."""
    },
    {
        "id": "herrah",
        "name_fa": "هرا وحش",
        "name_en": "Herrah the Beast",
        "type_fa": "رویابین (Dreamer)",
        "story_fa": """هرا، یکی از سه رویابین و ملکه‌ی تودرتوی عمیق (Deepnest) است. او مادر هورنت (Hornet) است و با پادشاه رنگ‌پریده ازدواج کرد تا بتواند فرزندی داشته باشد.

هرا برای محافظت از تودرتوی عمیق و فرزندانش، با فدا کردن خود، معبد تخم سیاه را مهروموم کرد. او در اعماق تودرتوی عمیق، در رؤیا زندانی است. شوالیه برای رسیدن به او، باید از تاریکی‌ها و خطرات Deepnest عبور کند."""
    },
]

# ============================================================
# درجه‌ی سختی
# ============================================================
DIFFICULTY = {
    "false_knight": 2, "gruz_mother": 1, "brooding_mawlek": 3,
    "vengefly_king": 2, "hornet": 3, "massive_moss_charger": 1,
    "elder_hu": 2, "uumuu": 3, "broken_vessel": 3,
    "xero": 2, "dung_defender": 2, "white_defender": 4,
    "flukemarm": 1, "crystal_guardian": 2, "mantis_lords": 4,
    "soul_warrior": 2, "nosk": 3, "watcher_knights": 4,
    "gorb": 1, "traitor_lord": 4, "marmu": 2,
    "galien": 2, "markoth": 3, "no_eyes": 2,
    "the_collector": 3, "god_tamer": 3, "hive_knight": 3,
    "zote_the_mighty": 1, "oblobbles": 3, "grimm": 5,
    "nightmare_king_grimm": 5, "paintmaster_sheo": 4,
    "great_nailsage_sly": 4, "pure_vessel": 5,
    "winged_nosk": 4, "radiance": 5,
    "brothers_oro_mato": 4, "the_hollow_knight": 5,
}

LOCATIONS = [
    ("all", "همه"),
    ("گذرگاه فراموش‌شده", "گذرگاه فراموش‌شده"),
    ("مسیر سبز", "مسیر سبز"),
    ("زباله‌های قارچی", "زباله‌های قارچی"),
    ("شهر اشک‌ها", "شهر اشک‌ها"),
    ("آبراه‌های سلطنتی", "آبراه‌های سلطنتی"),
    ("قله‌ی کریستال", "قله‌ی کریستال"),
    ("تودرتوی عمیق", "تودرتوی عمیق"),
    ("باغ‌های ملکه", "باغ‌های ملکه"),
    ("کولوسئوم", "کولوسئوم احمق‌ها"),
    ("کندو", "کندو"),
    ("چادر گریم", "چادر گریم"),
    ("Pantheon", "پانتئون"),
    ("معبد تخم سیاه", "معبد تخم سیاه"),
]

# ============================================================
# باس‌ها
# ============================================================
BOSSES = [
    {"id": "false_knight", "name_fa": "شوالیه دروغین", "name_en": "False Knight",
     "location_fa": "گذرگاه فراموش‌شده", "hp": 65,
     "attacks": [
         {"name": "پرش و کوبش", "desc": "می‌پرد و چکش سنگین را روی زمین می‌کوبد."},
         {"name": "چرخش", "desc": "به سمت شوالیه می‌چرخد و با سرعت حمله می‌کند."},
         {"name": "ریزش سنگ", "desc": "سنگ‌ها از سقف فرو می‌ریزند."},
     ],
     "prerequisites_fa": "ندارد؛ اولین باس داستانی.",
     "strategy_fa": "زیر پای او بایست و وقتی می‌پرد، جاخالی بده. بعد از هر پرش ۲ تا ۳ ضربه بزن.",
     "story_fa": "نگهبانی زره‌پوش که راه معبد تخم سیاه را می‌بندد.",
     "dream_version": "Failed Champion (قهرمان شکست‌خورده) — نسخه‌ی رؤیایی که با Dream Nail روی زره‌اش باز می‌شود."},
    {"id": "gruz_mother", "name_fa": "مادر گروز", "name_en": "Gruz Mother",
     "location_fa": "گذرگاه فراموش‌شده", "hp": 90,
     "attacks": [
         {"name": "شارژ هوایی", "desc": "با سرعت به سمت شوالیه پرواز می‌کند."},
         {"name": "بمباران گروز", "desc": "گروزهای کوچک از بدنش بیرون می‌ریزند."},
     ],
     "prerequisites_fa": "ندارد.",
     "strategy_fa": "وقتی روی زمین نشسته، فرصت طلایی حمله است.",
     "story_fa": "مادر گروز موجودی چاق و کند است که در گوشه‌ای از گذرگاه آرمیده.",
     "dream_version": None},
    {"id": "brooding_mawlek", "name_fa": "ماولک پرورش‌دهنده", "name_en": "Brooding Mawlek",
     "location_fa": "گذرگاه فراموش‌شده", "hp": 200,
     "attacks": [
         {"name": "پاشش عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
         {"name": "پنجه‌ی سنگین", "desc": "با پنجه ضربه می‌زند."},
         {"name": "فریاد", "desc": "با فریاد امواج ضربه‌ای می‌سازد."},
     ],
     "prerequisites_fa": "Mantis Claw برای رسیدن به اتاق مخفی.",
     "strategy_fa": "زیر بدنش بایست و از پاشش‌ها جاخالی بده.",
     "story_fa": "موجودی منزوی که در تاریکی زندگی می‌کند.",
     "dream_version": None},
    {"id": "vengefly_king", "name_fa": "پادشاه انتقام‌مگس", "name_en": "Vengefly King",
     "location_fa": "مسیر سبز", "hp": 90,
     "attacks": [
         {"name": "شیرجه", "desc": "به سمت شوالیه شیرجه می‌زند."},
         {"name": "احضار انتقام‌مگس", "desc": "انتقام‌مگس‌های کوچک احضار می‌کند."},
     ],
     "prerequisites_fa": "ندارد.",
     "strategy_fa": "روی سکوها بایست و از شیرجه جاخالی بده.",
     "story_fa": "پادشاه مگس‌های انتقام‌جو که در مسیر سبز لانه دارد.",
     "dream_version": None},
    {"id": "hornet", "name_fa": "هورنت", "name_en": "Hornet",
     "location_fa": "مسیر سبز", "hp": 90,
     "attacks": [
         {"name": "سوزن‌زنی", "desc": "با سرعت به سمت شوالیه می‌دود و ضربه می‌زند."},
         {"name": "پرتاب سوزن", "desc": "سوزن را پرتاب می‌کند و با نخ برمی‌گرداند."},
         {"name": "جهش", "desc": "به هوا می‌پرد و از بالا حمله می‌کند."},
     ],
     "prerequisites_fa": "ندارد؛ اولین دیدار داستانی.",
     "strategy_fa": "الگوی حمله‌اش قابل پیش‌بینی است. بعد از هر پرتاب سوزن، ۲ ضربه بزن.",
     "story_fa": "دختر پادشاه رنگ‌پریده و ملکه‌ی کندو.",
     "dream_version": "Hornet Sentinel — نسخه‌ی قوی‌تر هورنت در لبه‌ی پادشاهی."},
    {"id": "massive_moss_charger", "name_fa": "خزه‌ی عظیم مهاجم", "name_en": "Massive Moss Charger",
     "location_fa": "مسیر سبز", "hp": 100,
     "attacks": [
         {"name": "شارژ", "desc": "با سرعت به سمت شوالیه می‌دود."},
         {"name": "خزه‌پاشی", "desc": "خزه‌های کوچک پرتاب می‌کند."},
     ],
     "prerequisites_fa": "ندارد.",
     "strategy_fa": "وقتی شارژ می‌کند، بپر و از بالای سرش رد شو.",
     "story_fa": "توده‌ای عظیم از خزه که در مسیر سبز زندگی می‌کند.",
     "dream_version": None},
    {"id": "no_eyes", "name_fa": "بی‌چشم", "name_en": "No Eyes",
     "location_fa": "مسیر سبز", "hp": 200,
     "attacks": [
         {"name": "احضار ارواح", "desc": "ارواح کوچک احضار می‌کند."},
         {"name": "پرتاب نور", "desc": "نورهایی پرتاب می‌کند."},
     ],
     "prerequisites_fa": "Dream Nail.",
     "strategy_fa": "از ارواح جاخالی بده.",
     "story_fa": "رویابینی که در مسیر سبز زندانی شده است.",
     "dream_version": None},
    {"id": "elder_hu", "name_fa": "هو بزرگ", "name_en": "Elder Hu",
     "location_fa": "زباله‌های قارچی", "hp": 200,
     "attacks": [
         {"name": "حلقه‌های انرژی", "desc": "حلقه‌های انرژی پرتاب می‌کند."},
         {"name": "تله‌ی نوری", "desc": "نورهایی روی زمین می‌سازد که آسیب می‌زنند."},
     ],
     "prerequisites_fa": "Dream Nail برای ورود به رؤیا.",
     "strategy_fa": "بین حلقه‌ها جاخالی بده و با Dash Slash حمله کن.",
     "story_fa": "رویابین (Dreamer) که در رؤیا زندانی شده است.",
     "dream_version": None},
    {"id": "mantis_lords", "name_fa": "اربابان مانتیس", "name_en": "Mantis Lords",
     "location_fa": "زباله‌های قارچی", "hp": 210,
     "attacks": [
         {"name": "سوزن‌زنی", "desc": "با سرعت به سمت شوالیه می‌دوند."},
         {"name": "پرتاب سوزن", "desc": "سوزن‌ها را پرتاب می‌کنند."},
         {"name": "جهش", "desc": "از بالا حمله می‌کنند."},
     ],
     "prerequisites_fa": "Mantis Claw.",
     "strategy_fa": "اول دو ارباب اول را بکش.",
     "story_fa": "سه ارباب مانتیس که از دهکده‌شان محافظت می‌کنند.",
     "dream_version": "Sisters of Battle — نسخه‌ی سه‌نفره در Pantheon of Hallownest."},
    {"id": "soul_warrior", "name_fa": "جنگجوی روح", "name_en": "Soul Warrior",
     "location_fa": "شهر اشک‌ها", "hp": 200,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زند."},
         {"name": "توپ روح", "desc": "توپ روح پرتاب می‌کند."},
         {"name": "جهش", "desc": "می‌پرد و حمله می‌کند."},
     ],
     "prerequisites_fa": "ندارد.",
     "strategy_fa": "بعد از هر حمله‌اش ضربه بزن.",
     "story_fa": "جنگجویی که از معبد روح محافظت می‌کند.",
     "dream_version": None},
    {"id": "the_collector", "name_fa": "جمع‌کننده", "name_en": "The Collector",
     "location_fa": "شهر اشک‌ها", "hp": 300,
     "attacks": [
         {"name": "احضار موجودات", "desc": "موجودات را از شیشه بیرون می‌آورد."},
         {"name": "پرش", "desc": "می‌پرد و حمله می‌کند."},
     ],
     "prerequisites_fa": "دسترسی به برج نگهبان.",
     "strategy_fa": "ابتدا موجودات احضارشده را بکش.",
     "story_fa": "موجودی که موجودات مختلف را در شیشه جمع می‌کند.",
     "dream_version": None},
    {"id": "watcher_knights", "name_fa": "شوالیه‌های نگهبان", "name_en": "Watcher Knights",
     "location_fa": "شهر اشک‌ها", "hp": 220,
     "attacks": [
         {"name": "غلت", "desc": "به سمت شوالیه غلت می‌زنند."},
         {"name": "پرش", "desc": "می‌پرند و ضربه می‌زنند."},
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر حمله می‌کنند."},
     ],
     "prerequisites_fa": "دسترسی به برج نگهبان.",
     "strategy_fa": "قبل از ورود، یکی از زنجیرها را ببر.",
     "story_fa": "شش شوالیه‌ی زره‌پوش که از برج نگهبان محافظت می‌کنند.",
     "dream_version": None},
    {"id": "dung_defender", "name_fa": "مدافع سرگین", "name_en": "Dung Defender",
     "location_fa": "آبراه‌های سلطنتی", "hp": 250,
     "attacks": [
         {"name": "پرتاب سرگین", "desc": "توپ‌های سرگین پرتاب می‌کند."},
         {"name": "غلت", "desc": "به سمت شوالیه غلت می‌زند."},
         {"name": "فرو رفتن", "desc": "در زمین فرو می‌رود و از جای دیگر بیرون می‌آید."},
     ],
     "prerequisites_fa": "ندارد (اختیاری).",
     "strategy_fa": "وقتی از زمین بیرون می‌آید، سریع ضربه بزن.",
     "story_fa": "یکی از پنج شوالیه‌ی پادشاه رنگ‌پریده که در آبراه‌ها پنهان شده است.",
     "dream_version": "White Defender — نسخه‌ی رؤیایی با حملات سریع‌تر."},
    {"id": "white_defender", "name_fa": "مدافع سفید", "name_en": "White Defender",
     "location_fa": "آبراه‌های سلطنتی", "hp": 350,
     "attacks": [
         {"name": "پرتاب سرگین سفید", "desc": "توپ‌های سفید پرتاب می‌کند."},
         {"name": "غلت سریع", "desc": "سریع‌تر از نسخه‌ی اصلی غلت می‌زند."},
         {"name": "زمین‌لرزه", "desc": "زمین را می‌لرزاند."},
     ],
     "prerequisites_fa": "Dream Nail و شکست Dung Defender.",
     "strategy_fa": "مثل نسخه‌ی اصلی اما سریع‌تر.",
     "story_fa": "نسخه‌ی رؤیایی مدافع سرگین در اوج قدرت.",
     "dream_version": None},
    {"id": "flukemarm", "name_fa": "مادر فلوک", "name_en": "Flukemarm",
     "location_fa": "آبراه‌های سلطنتی", "hp": 150,
     "attacks": [
         {"name": "احضار فلوک", "desc": "فلوک‌های کوچک بی‌پایان احضار می‌کند."},
     ],
     "prerequisites_fa": "ندارد.",
     "strategy_fa": "سریع به سمتش برو و با ضربات پیاپی بکشش.",
     "story_fa": "مادر فلوک‌ها که در آبراه‌ها زندگی می‌کند.",
     "dream_version": None},
    {"id": "crystal_guardian", "name_fa": "نگهبان کریستال", "name_en": "Crystal Guardian",
     "location_fa": "قله‌ی کریستال", "hp": 280,
     "attacks": [
         {"name": "لیزر کریستالی", "desc": "پرتو کریستالی شلیک می‌کند."},
         {"name": "پرش", "desc": "می‌پرد و به زمین می‌کوبد."},
     ],
     "prerequisites_fa": "Mantis Claw.",
     "strategy_fa": "وقتی لیزر می‌زند، بپر و به بالای سرش برو و ضربه بزن.",
     "story_fa": "نگهبانی که توسط کریستال‌های قله تسخیر شده است.",
     "dream_version": "Enraged Guardian — نسخه‌ی دوم در قله‌ی کریستال."},
    {"id": "xero", "name_fa": "زرو", "name_en": "Xero",
     "location_fa": "شهر اشک‌ها", "hp": 200,
     "attacks": [
         {"name": "پرتاب شمشیر", "desc": "شمشیرهای نورانی پرتاب می‌کند."},
         {"name": "شمشیرهای معلق", "desc": "شمشیرها را در هوا معلق می‌کند."},
     ],
     "prerequisites_fa": "Dream Nail.",
     "strategy_fa": "بین شمشیرها جاخالی بده و بعد از هر پرتاب حمله کن.",
     "story_fa": "رویابین خائن که توسط پادشاه رنگ‌پریده محکوم شد.",
     "dream_version": None},
    {"id": "nosk", "name_fa": "نوسک", "name_en": "Nosk",
     "location_fa": "تودرتوی عمیق", "hp": 300,
     "attacks": [
         {"name": "شبیه‌سازی", "desc": "خود را شبیه شوالیه می‌کند و حمله می‌کند."},
         {"name": "پرش", "desc": "از سقف می‌پرد و حمله می‌کند."},
         {"name": "عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
     ],
     "prerequisites_fa": "دسترسی به تودرتوی عمیق.",
     "strategy_fa": "وقتی از سقف می‌پرد، زیرش بایست و ضربه بزن.",
     "story_fa": "موجودی که خود را شبیه قربانیانش می‌کند.",
     "dream_version": None},
    {"id": "galien", "name_fa": "گالین", "name_en": "Galien",
     "location_fa": "تودرتوی عمیق", "hp": 200,
     "attacks": [
         {"name": "پرتاب داس", "desc": "داس‌های نورانی پرتاب می‌کند."},
         {"name": "داس چرخان", "desc": "داس را دور خودش می‌چرخاند."},
     ],
     "prerequisites_fa": "Dream Nail.",
     "strategy_fa": "از داس‌ها جاخالی بده.",
     "story_fa": "رویابینی که در تودرتوی عمیق زندانی شده است.",
     "dream_version": None},
    {"id": "gorb", "name_fa": "گورب", "name_en": "Gorb",
     "location_fa": "مسیر سبز", "hp": 150,
     "attacks": [
         {"name": "پرتاب نور", "desc": "نورهایی پرتاب می‌کند."},
         {"name": "موج", "desc": "امواج ضربه‌ای می‌سازد."},
     ],
     "prerequisites_fa": "Dream Nail.",
     "strategy_fa": "بین نورها جاخالی بده.",
     "story_fa": "رویابینی که در صخره‌های زوزه‌کش زندانی شده است.",
     "dream_version": None},
    {"id": "markoth", "name_fa": "مارکوث", "name_en": "Markoth",
     "location_fa": "تودرتوی عمیق", "hp": 250,
     "attacks": [
         {"name": "پرتاب شمشیر", "desc": "شمشیرهای نورانی پرتاب می‌کند."},
         {"name": "سپر", "desc": "سپر نورانی دور خودش می‌چرخاند."},
     ],
     "prerequisites_fa": "Dream Nail.",
     "strategy_fa": "بین شمشیرها جاخالی بده.",
     "story_fa": "رویابینی که در لبه‌ی پادشاهی زندانی شده است.",
     "dream_version": None},
    {"id": "traitor_lord", "name_fa": "ارباب خائن", "name_en": "Traitor Lord",
     "location_fa": "باغ‌های ملکه", "hp": 400,
     "attacks": [
         {"name": "پنجه", "desc": "با پنجه ضربه می‌زند."},
         {"name": "موج", "desc": "امواج ضربه‌ای می‌فرستد."},
         {"name": "پرش", "desc": "می‌پرد و حمله می‌کند."},
     ],
     "prerequisites_fa": "Mantis Claw و دسترسی به باغ‌های ملکه.",
     "strategy_fa": "از امواج با پرش جاخالی بده.",
     "story_fa": "ارباب مانتیسی که به ملکه خیانت کرد.",
     "dream_version": None},
    {"id": "marmu", "name_fa": "مارمو", "name_en": "Marmu",
     "location_fa": "باغ‌های ملکه", "hp": 200,
     "attacks": [
         {"name": "غلت", "desc": "به سمت شوالیه غلت می‌زند."},
         {"name": "پرش", "desc": "می‌پرد و ضربه می‌زند."},
     ],
     "prerequisites_fa": "Dream Nail.",
     "strategy_fa": "وقتی غلت می‌زند، بپر و از بالای سرش رد شو.",
     "story_fa": "رویابین کوچکی که در باغ‌های ملکه بازی می‌کند.",
     "dream_version": None},
    {"id": "god_tamer", "name_fa": "رام‌کننده‌ی خدا", "name_en": "God Tamer",
     "location_fa": "کولوسئوم احمق‌ها", "hp": 300,
     "attacks": [
         {"name": "پرتاب نیزه", "desc": "نیزه پرتاب می‌کند."},
         {"name": "حیوان", "desc": "حیوانش حمله می‌کند."},
     ],
     "prerequisites_fa": "ورود به کولوسئوم احمق‌ها.",
     "strategy_fa": "ابتدا حیوانش را بکش.",
     "story_fa": "رام‌کننده‌ای که در کولوسئوم احمق‌ها مبارزه می‌کند.",
     "dream_version": None},
    {"id": "zote_the_mighty", "name_fa": "زوت توانا", "name_en": "Zote the Mighty",
     "location_fa": "کولوسئوم احمق‌ها", "hp": 100,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زند."},
         {"name": "فریاد", "desc": "فریاد می‌زند."},
     ],
     "prerequisites_fa": "ورود به کولوسئوم احمق‌ها.",
     "strategy_fa": "زوت بسیار ضعیف است. سریع بکشش.",
     "story_fa": "شوالیه‌ای که ادعای قدرت می‌کند اما بسیار ضعیف است.",
     "dream_version": "Grey Prince Zote — نسخه‌ی رؤیایی در Dirtmouth."},
    {"id": "oblobbles", "name_fa": "اُبلابل‌ها", "name_en": "Oblobbles",
     "location_fa": "کولوسئوم احمق‌ها", "hp": 200,
     "attacks": [
         {"name": "پرتاب عفونت", "desc": "توپ‌های عفونت پرتاب می‌کنند."},
         {"name": "غلت", "desc": "به سمت شوالیه غلت می‌زنند."},
     ],
     "prerequisites_fa": "ورود به کولوسئوم احمق‌ها.",
     "strategy_fa": "ابتدا یکی را بکش، سپس به دومی برو.",
     "story_fa": "دو موجود چاق که در کولوسئوم مبارزه می‌کنند.",
     "dream_version": None},
    {"id": "hive_knight", "name_fa": "شوالیه‌ی کندو", "name_en": "Hive Knight",
     "location_fa": "کندو", "hp": 350,
     "attacks": [
         {"name": "ضربه‌ی نیزه", "desc": "با نیزه ضربه می‌زند."},
         {"name": "پرتاب نیزه", "desc": "نیزه پرتاب می‌کند."},
         {"name": "پرش", "desc": "می‌پرد و حمله می‌کند."},
     ],
     "prerequisites_fa": "دسترسی به کندو.",
     "strategy_fa": "بعد از هر حمله‌اش ضربه بزن.",
     "story_fa": "نگهبان کندو که از ملکه محافظت می‌کند.",
     "dream_version": None},
    {"id": "uumuu", "name_fa": "اوومو", "name_en": "Uumuu",
     "location_fa": "شهر اشک‌ها", "hp": 300,
     "attacks": [
         {"name": "شوک الکتریکی", "desc": "الکتریسیته در آب پخش می‌کند."},
         {"name": "احضار اوما", "desc": "اوماهای کوچک احضار می‌کند."},
     ],
     "prerequisites_fa": "Isma's Tear برای عبور از آب اسیدی.",
     "strategy_fa": "با ضربه زدن به اوماها آن‌ها را به سمت اوومو پرتاب کن.",
     "story_fa": "نگهبان آرشیوهای معلم که از دانش ملکه محافظت می‌کند.",
     "dream_version": None},
    {"id": "broken_vessel", "name_fa": "ظرف شکسته", "name_en": "Broken Vessel",
     "location_fa": "شهر اشک‌ها", "hp": 250,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زند."},
         {"name": "پرش و کوبش", "desc": "می‌پرد و به زمین می‌کوبد."},
         {"name": "عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
     ],
     "prerequisites_fa": "Mantis Claw و دسترسی به حوضه‌ی باستانی.",
     "strategy_fa": "زیرش بایست و بعد از هر پرش ضربه بزن.",
     "story_fa": "یکی از ظرف‌های (Vessel) شکسته که عفونت در آن رخنه کرده است.",
     "dream_version": "Lost Kin — نسخه‌ی رؤیایی در حوضه‌ی باستانی."},
    {"id": "grimm", "name_fa": "استاد گروه گریم", "name_en": "Troupe Master Grimm",
     "location_fa": "چادر گریم", "hp": 800,
     "attacks": [
         {"name": "شیرجه", "desc": "به سمت شوالیه شیرجه می‌زند."},
         {"name": "پرتاب خفاش", "desc": "خفاش‌های آتشین پرتاب می‌کند."},
         {"name": "ستون آتش", "desc": "ستون‌های آتش از زمین بیرون می‌آورد."},
     ],
     "prerequisites_fa": "احضار گروه گریم با Grimmchild.",
     "strategy_fa": "بعد از هر شیرجه ۲ ضربه بزن.",
     "story_fa": "استاد گروه گریم که در چادری در Dirtmouth مبارزه می‌کند.",
     "dream_version": "Nightmare King Grimm — سخت‌ترین باس بازی."},
    {"id": "nightmare_king_grimm", "name_fa": "پادشاه کابوس گریم", "name_en": "Nightmare King Grimm",
     "location_fa": "چادر گریم", "hp": 1400,
     "attacks": [
         {"name": "شیرجه‌ی سریع", "desc": "سریع‌تر شیرجه می‌زند."},
         {"name": "خفاش‌های آتشین", "desc": "خفاش‌های بیشتری پرتاب می‌کند."},
         {"name": "ستون‌های آتش", "desc": "ستون‌های آتش بیشتری می‌سازد."},
         {"name": "توپ‌های آتشین", "desc": "توپ‌های آتشین پرتاب می‌کند."},
     ],
     "prerequisites_fa": "شکست Troupe Master Grimm.",
     "strategy_fa": "سخت‌ترین باس بازی. باید الگوهایش را حفظ کنی.",
     "story_fa": "نسخه‌ی کابوسی گریم در اوج قدرت.",
     "dream_version": None},
    {"id": "paintmaster_sheo", "name_fa": "استاد نقاشی شئو", "name_en": "Paintmaster Sheo",
     "location_fa": "Pantheon of Hallownest", "hp": 600,
     "attacks": [
         {"name": "ضربه‌ی قلم‌مو", "desc": "با قلم‌مو ضربه می‌زند."},
         {"name": "پرتاب رنگ", "desc": "رنگ‌ها را پرتاب می‌کند."},
         {"name": "موج رنگ", "desc": "امواج رنگ می‌سازد."},
     ],
     "prerequisites_fa": "ورود به Pantheon of Hallownest.",
     "strategy_fa": "از رنگ‌ها جاخالی بده.",
     "story_fa": "نقاشی که در پانتئون مبارزه می‌کند.",
     "dream_version": None},
    {"id": "great_nailsage_sly", "name_fa": "استاد بزرگ میخ‌ها اسلای", "name_en": "Great Nailsage Sly",
     "location_fa": "Pantheon of Hallownest", "hp": 700,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زند."},
         {"name": "پرش", "desc": "می‌پرد و حمله می‌کند."},
         {"name": "موج", "desc": "امواج ضربه‌ای می‌سازد."},
     ],
     "prerequisites_fa": "ورود به Pantheon of Hallownest.",
     "strategy_fa": "الگوهایش قابل پیش‌بینی است.",
     "story_fa": "استاد بزرگ میخ‌ها که در پانتئون مبارزه می‌کند.",
     "dream_version": None},
    {"id": "pure_vessel", "name_fa": "ظرف خالص", "name_en": "Pure Vessel",
     "location_fa": "Pantheon of Hallownest", "hp": 1000,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زند."},
         {"name": "پرش", "desc": "می‌پرد و حمله می‌کند."},
         {"name": "موج", "desc": "امواج ضربه‌ای می‌سازد."},
         {"name": "عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
     ],
     "prerequisites_fa": "ورود به Pantheon of Hallownest.",
     "strategy_fa": "سخت‌ترین باس پانتئون. باید الگوهایش را حفظ کنی.",
     "story_fa": "نسخه‌ی خالص هالو نایت در اوج قدرت.",
     "dream_version": None},
    {"id": "winged_nosk", "name_fa": "نوسک بال‌دار", "name_en": "Winged Nosk",
     "location_fa": "Pantheon of Hallownest", "hp": 800,
     "attacks": [
         {"name": "شبیه‌سازی", "desc": "خود را شبیه شوالیه می‌کند."},
         {"name": "پرش", "desc": "از سقف می‌پرد."},
         {"name": "عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
     ],
     "prerequisites_fa": "ورود به Pantheon of Hallownest.",
     "strategy_fa": "مثل نوسک اصلی اما سریع‌تر.",
     "story_fa": "نسخه‌ی بال‌دار نوسک در پانتئون.",
     "dream_version": None},
    {"id": "brothers_oro_mato", "name_fa": "برادران اورو و ماتو", "name_en": "Brothers Oro & Mato",
     "location_fa": "Pantheon of Hallownest", "hp": 500,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زنند."},
         {"name": "پرش", "desc": "می‌پرند و حمله می‌کنند."},
         {"name": "موج", "desc": "امواج ضربه‌ای می‌سازند."},
     ],
     "prerequisites_fa": "ورود به Pantheon of Hallownest.",
     "strategy_fa": "ابتدا یکی را بکش، سپس به دومی برو.",
     "story_fa": "دو برادر شمشیرزن که در پانتئون مبارزه می‌کنند.",
     "dream_version": None},
    {"id": "radiance", "name_fa": "درخشش", "name_en": "The Radiance",
     "location_fa": "معبد تخم سیاه", "hp": 1500,
     "attacks": [
         {"name": "پرتو نور", "desc": "پرتوهای نور از آسمان می‌بارد."},
         {"name": "شمشیرهای نور", "desc": "شمشیرهای نور پرتاب می‌کند."},
         {"name": "موج نور", "desc": "امواج نور می‌سازد."},
         {"name": "عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
     ],
     "prerequisites_fa": "داشتن Void Heart و شکست هالو نایت.",
     "strategy_fa": "سخت‌ترین باس داستانی. باید از پرتوها جاخالی بدهی.",
     "story_fa": "موجود الهی که توسط پادشاه رنگ‌پریده فراموش شد.",
     "dream_version": "Absolute Radiance — نسخه‌ی نهایی در Pantheon of Hallownest."},
    {"id": "the_hollow_knight", "name_fa": "شوالیه‌ی توخالی", "name_en": "The Hollow Knight",
     "location_fa": "معبد تخم سیاه", "hp": 1500,
     "attacks": [
         {"name": "ضربه‌ی شمشیر", "desc": "با شمشیر ضربه می‌زند."},
         {"name": "پرش", "desc": "می‌پرد و حمله می‌کند."},
         {"name": "عفونت", "desc": "توپ‌های عفونت پرتاب می‌کند."},
         {"name": "خودزنی", "desc": "به خودش ضربه می‌زند و عفونت پخش می‌کند."},
     ],
     "prerequisites_fa": "ندارد؛ باس داستانی نهایی.",
     "strategy_fa": "سخت‌ترین باس داستانی. بعد از هر حمله‌اش ۲ ضربه بزن.",
     "story_fa": "ظرف خالصی که رادیانس را در خود زندانی کرده، ولی عفونت در آن رخنه کرده است.",
     "dream_version": None},
]


def stars_html(n):
    out = ""
    for i in range(1, 6):
        if i <= n:
            out += '<span style="color:#b8956a;">★</span>'
        else:
            out += '<span style="color:#333;">★</span>'
    return out


def find_map_image():
    if not os.path.exists("map"):
        return None
    files = os.listdir("map")
    for f in files:
        if is_image(f):
            return f
    return None


CSS = """
:root{--bg-dark:#0a0a0f;--bg-card:#12121a;--text-primary:#e8e6e3;--text-secondary:#9a9a9a;--accent:#b8956a;--accent-bright:#d4a97a;--accent-glow:rgba(184,149,106,0.35);--border:#2a2a35;--dream:#b895d4;--void:#6a4a9a;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg-dark);color:var(--text-primary);line-height:1.9;min-height:100vh;overflow-x:hidden;}
#particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}
.particle{position:absolute;background:var(--accent);border-radius:50%;opacity:0.3;animation:float linear infinite;}
@keyframes float{0%{transform:translateY(0);opacity:0;}10%{opacity:0.5;}90%{opacity:0.5;}100%{transform:translateY(-100vh) translateX(50px);opacity:0;}}
.navbar{display:flex;justify-content:space-between;align-items:center;padding:1.2rem 4rem;background:rgba(10,10,15,0.92);backdrop-filter:blur(12px);position:sticky;top:0;z-index:50;border-bottom:1px solid var(--border);flex-wrap:wrap;gap:1rem;}
.nav-brand{font-size:1.3rem;font-weight:900;letter-spacing:2px;color:var(--accent);display:flex;align-items:center;gap:0.5rem;}
.brand-icon{font-size:1.5rem;filter:drop-shadow(0 0 8px var(--accent-glow));}
.nav-links{display:flex;gap:1.5rem;list-style:none;flex-wrap:wrap;}
.nav-links a{color:var(--text-secondary);text-decoration:none;transition:color 0.3s;font-weight:400;}
.nav-links a:hover{color:var(--accent-bright);}
.nav-links a.active{color:var(--accent);font-weight:700;}
.hamburger{display:none;background:none;border:2px solid var(--accent);color:var(--accent);font-size:1.5rem;padding:0.4rem 0.8rem;border-radius:6px;cursor:pointer;font-family:inherit;}
main{min-height:70vh;position:relative;z-index:1;}
.hero{min-height:80vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:4rem 2rem;background:linear-gradient(180deg,rgba(10,10,15,0.6) 0%,var(--bg-dark) 100%);position:relative;}
.hero-title{font-size:clamp(3rem,8vw,5.5rem);font-weight:900;color:var(--accent);text-shadow:0 0 50px var(--accent-glow);letter-spacing:4px;margin-bottom:1rem;}
.hero-subtitle{font-size:1.3rem;color:var(--text-secondary);margin-bottom:2.5rem;}
.hero-buttons{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;}
.btn-primary,.btn-secondary{display:inline-block;padding:0.9rem 2.2rem;text-decoration:none;font-weight:700;font-size:1rem;border-radius:6px;transition:all 0.3s ease;cursor:pointer;border:2px solid transparent;font-family:'Vazirmatn',sans-serif;}
.btn-primary{background:var(--accent);color:var(--bg-dark);border-color:var(--accent);}
.btn-primary:hover{background:var(--accent-bright);box-shadow:0 0 30px var(--accent-glow);transform:translateY(-2px);}
.btn-secondary{background:transparent;border-color:var(--border);color:var(--text-secondary);}
.btn-secondary:hover{border-color:var(--accent);color:var(--accent);}
.section{padding:5rem 4rem;max-width:1400px;margin:0 auto;position:relative;z-index:1;}
.section-title{font-size:2.5rem;color:var(--accent);margin-bottom:3rem;text-align:center;position:relative;padding-bottom:1rem;}
.section-title::after{content:'';position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:80px;height:3px;background:var(--accent);border-radius:2px;}
.story-content{max-width:900px;margin:0 auto;font-size:1.1rem;color:var(--text-secondary);white-space:pre-line;line-height:2.2;background:var(--bg-card);padding:3rem;border-radius:12px;border:1px solid var(--border);}
.center-btn{text-align:center;margin-top:2rem;}
.search-bar{max-width:600px;margin:0 auto 2rem;position:relative;}
.search-bar input{width:100%;padding:1rem 3rem 1rem 1.5rem;background:var(--bg-card);border:2px solid var(--border);border-radius:50px;color:var(--text-primary);font-family:'Vazirmatn',sans-serif;font-size:1rem;transition:all 0.3s;}
.search-bar input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow);}
.filter-bar{display:flex;flex-wrap:wrap;gap:0.8rem;justify-content:center;margin-bottom:3rem;}
.filter-btn{padding:0.6rem 1.4rem;background:var(--bg-card);border:1px solid var(--border);border-radius:50px;color:var(--text-secondary);cursor:pointer;font-family:'Vazirmatn',sans-serif;font-size:0.9rem;transition:all 0.3s;}
.filter-btn:hover{border-color:var(--accent);color:var(--accent);}
.filter-btn.active{background:var(--accent);color:var(--bg-dark);border-color:var(--accent);}
.bosses-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1.8rem;}
.boss-card{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;overflow:hidden;text-decoration:none;transition:transform 0.35s,border-color 0.35s,box-shadow 0.35s;display:flex;flex-direction:column;}
.boss-card:hover{transform:translateY(-8px);border-color:var(--accent);box-shadow:0 20px 45px rgba(0,0,0,0.6),0 0 30px var(--accent-glow);}
.boss-card-image{height:200px;overflow:hidden;background:radial-gradient(circle at center,#1e1e2a 0%,#0e0e15 100%);display:flex;align-items:center;justify-content:center;padding:1rem;}
.boss-card-image img,.boss-card-image svg{max-width:100%;max-height:100%;object-fit:contain;transition:transform 0.5s;}
.boss-card:hover .boss-card-image img,.boss-card:hover .boss-card-image svg{transform:scale(1.15);}
.boss-card-content{padding:1.4rem;text-align:center;}
.boss-name-fa{font-size:1.15rem;color:var(--text-primary);margin-bottom:0.3rem;}
.boss-name-en{font-size:0.85rem;color:var(--accent);direction:ltr;letter-spacing:1px;margin-bottom:0.7rem;font-weight:400;}
.boss-location{font-size:0.85rem;color:var(--text-secondary);margin-bottom:0.5rem;}
.no-results{text-align:center;color:var(--text-secondary);padding:3rem;font-size:1.2rem;display:none;}
.boss-detail{padding-top:3rem;}
.boss-header{display:flex;gap:3rem;align-items:center;margin-bottom:4rem;flex-wrap:wrap;}
.boss-image-large{width:300px;height:300px;background:radial-gradient(circle at center,#1e1e2a 0%,#0e0e15 100%);border:1px solid var(--border);border-radius:16px;display:flex;align-items:center;justify-content:center;padding:1.5rem;flex-shrink:0;}
.boss-image-large img,.boss-image-large svg{max-width:100%;max-height:100%;object-fit:contain;}
.boss-title-fa{font-size:3rem;color:var(--accent);margin-bottom:0.5rem;}
.boss-title-en{font-size:1.4rem;color:var(--text-secondary);direction:ltr;letter-spacing:2px;margin-bottom:1.5rem;font-weight:400;}
.boss-meta{display:flex;gap:2rem;flex-wrap:wrap;}
.meta-item{background:var(--bg-card);padding:0.6rem 1.2rem;border-radius:8px;border:1px solid var(--border);color:var(--text-primary);}
.boss-section{margin-bottom:3rem;}
.boss-section h2{color:var(--accent);font-size:1.5rem;margin-bottom:1.2rem;padding-right:1rem;border-right:4px solid var(--accent);}
.dream-section{background:linear-gradient(135deg,rgba(100,50,150,0.2) 0%,rgba(50,20,80,0.2) 100%);border:2px solid #6a4a9a;border-radius:12px;padding:2rem;margin-bottom:3rem;}
.dream-section h2{color:var(--dream);border-right-color:var(--dream);font-size:1.5rem;margin-bottom:1rem;padding-right:1rem;border-right:4px solid var(--dream);}
.dream-section p{color:#d4c4e3;line-height:2;}
.attacks-list{list-style:none;}
.attack-item{padding:1.2rem;background:var(--bg-card);border:1px solid var(--border);border-radius:10px;margin-bottom:0.8rem;}
.attack-item strong{color:var(--accent-bright);}
.video-wrapper{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;border:1px solid var(--border);box-shadow:0 20px 40px rgba(0,0,0,0.5);}
.video-wrapper iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:none;}
.map-container{max-width:100%;margin:0 auto;background:var(--bg-card);border:2px solid var(--accent);border-radius:14px;padding:1rem;box-shadow:0 0 40px var(--accent-glow);}
.map-container img{width:100%;height:auto;border-radius:8px;display:block;}
.regions-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;margin-top:2rem;}
.region-card{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:1.2rem;text-align:center;color:var(--text-secondary);font-size:0.95rem;transition:all 0.3s;}
.region-card:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-5px);}

/* === صفحه‌ی تاریخ === */
.lore-section{max-width:1000px;margin:0 auto 4rem;background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:2.5rem;transition:all 0.3s;}
.lore-section:hover{border-color:var(--accent);box-shadow:0 10px 30px rgba(0,0,0,0.5);}
.lore-header{display:flex;gap:2rem;align-items:center;margin-bottom:2rem;flex-wrap:wrap;}
.lore-image{width:150px;height:150px;border-radius:12px;background:radial-gradient(circle at center,#1e1e2a 0%,#0e0e15 100%);border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;padding:0.8rem;flex-shrink:0;overflow:hidden;}
.lore-image img{max-width:100%;max-height:100%;object-fit:contain;}
.lore-image svg{max-width:100%;max-height:100%;}
.lore-info{flex:1;min-width:200px;}
.lore-title-fa{font-size:1.8rem;color:var(--accent);margin-bottom:0.3rem;}
.lore-title-en{font-size:1rem;color:var(--text-secondary);direction:ltr;letter-spacing:1px;margin-bottom:0.5rem;font-weight:400;}
.lore-type{display:inline-block;background:rgba(184,149,106,0.2);color:var(--accent-bright);padding:0.3rem 0.9rem;border-radius:20px;font-size:0.85rem;border:1px solid var(--accent);}
.lore-text{color:var(--text-secondary);line-height:2.2;white-space:pre-line;font-size:1.05rem;}

/* === صفحه‌ی شوالیه === */
.knight-hero{display:flex;gap:3rem;align-items:center;justify-content:center;flex-wrap:wrap;background:linear-gradient(135deg,rgba(184,149,106,0.1) 0%,rgba(106,74,154,0.1) 100%);border:1px solid var(--border);border-radius:20px;padding:3rem;margin-bottom:4rem;position:relative;overflow:hidden;}
.knight-hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(184,149,106,0.15) 0%,transparent 50%);animation:rotate 20s linear infinite;pointer-events:none;}
@keyframes rotate{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
.knight-hero-image{width:280px;height:280px;border-radius:20px;background:radial-gradient(circle at center,#1e1e2a 0%,#0e0e15 100%);border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;padding:1rem;flex-shrink:0;position:relative;z-index:1;box-shadow:0 0 60px var(--accent-glow);}
.knight-hero-image img{max-width:100%;max-height:100%;object-fit:contain;filter:drop-shadow(0 0 20px rgba(184,149,106,0.5));}
.knight-hero-info{flex:1;min-width:280px;position:relative;z-index:1;}
.knight-hero-title{font-size:3.5rem;color:var(--accent);margin-bottom:0.5rem;text-shadow:0 0 30px var(--accent-glow);}
.knight-hero-subtitle{font-size:1.3rem;color:var(--text-secondary);direction:ltr;letter-spacing:2px;margin-bottom:1.5rem;}
.knight-hero-tags{display:flex;gap:0.8rem;flex-wrap:wrap;margin-top:1rem;}
.knight-tag{background:rgba(184,149,106,0.15);border:1px solid var(--accent);color:var(--accent-bright);padding:0.4rem 1rem;border-radius:20px;font-size:0.9rem;}

/* === گالری شوالیه === */
.knight-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1.5rem;margin-top:2rem;}
.gallery-item{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;overflow:hidden;transition:all 0.4s;cursor:pointer;position:relative;}
.gallery-item:hover{transform:translateY(-8px) scale(1.02);border-color:var(--accent);box-shadow:0 20px 45px rgba(0,0,0,0.6),0 0 30px var(--accent-glow);}
.gallery-item img{width:100%;height:250px;object-fit:cover;display:block;transition:transform 0.5s;}
.gallery-item:hover img{transform:scale(1.1);}
.gallery-caption{padding:1rem;text-align:center;color:var(--text-secondary);font-size:0.9rem;background:var(--bg-card);}

/* === توانایی‌ها === */
.abilities-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem;margin-top:2rem;}
.ability-card{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:1.5rem;transition:all 0.3s;position:relative;overflow:hidden;}
.ability-card:hover{border-color:var(--accent);transform:translateY(-5px);box-shadow:0 15px 35px rgba(0,0,0,0.5);}
.ability-card::before{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:var(--accent);opacity:0.3;transition:opacity 0.3s;}
.ability-card:hover::before{opacity:1;}
.ability-icon{font-size:2.5rem;margin-bottom:0.8rem;display:block;}
.ability-name-fa{font-size:1.2rem;color:var(--accent);margin-bottom:0.3rem;}
.ability-name-en{font-size:0.9rem;color:var(--text-secondary);direction:ltr;letter-spacing:1px;margin-bottom:1rem;}
.ability-desc{color:var(--text-secondary);font-size:0.95rem;line-height:1.9;}

/* === مسیر سفر === */
.journey-timeline{position:relative;max-width:900px;margin:3rem auto;padding-right:3rem;}
.journey-timeline::before{content:'';position:absolute;right:15px;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--accent) 0%,var(--void) 100%);border-radius:2px;}
.journey-item{position:relative;margin-bottom:2.5rem;padding-right:3rem;}
.journey-item::before{content:'';position:absolute;right:-8px;top:1.5rem;width:20px;height:20px;border-radius:50%;background:var(--bg-dark);border:3px solid var(--accent);z-index:1;box-shadow:0 0 15px var(--accent-glow);}
.journey-item:hover::before{background:var(--accent);}
.journey-card{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;transition:all 0.3s;}
.journey-card:hover{border-color:var(--accent);transform:translateX(-5px);box-shadow:0 10px 30px rgba(0,0,0,0.5);}
.journey-icon{font-size:2rem;margin-bottom:0.5rem;display:block;}
.journey-region-fa{font-size:1.3rem;color:var(--accent);margin-bottom:0.2rem;}
.journey-region-en{font-size:0.9rem;color:var(--text-secondary);direction:ltr;margin-bottom:0.8rem;}
.journey-desc{color:var(--text-secondary);font-size:0.95rem;}

/* === پایان‌ها === */
.endings-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.5rem;margin-top:2rem;}
.ending-card{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:2rem;transition:all 0.3s;position:relative;}
.ending-card:hover{border-color:var(--accent);transform:translateY(-5px);box-shadow:0 15px 35px rgba(0,0,0,0.5);}
.ending-icon{font-size:3rem;margin-bottom:1rem;display:block;text-align:center;}
.ending-name-fa{font-size:1.4rem;color:var(--accent);text-align:center;margin-bottom:0.3rem;}
.ending-name-en{font-size:1rem;color:var(--text-secondary);text-align:center;direction:ltr;margin-bottom:1.2rem;font-weight:400;}
.ending-desc{color:var(--text-secondary);font-size:0.95rem;line-height:1.9;margin-bottom:1rem;}
.ending-req{display:inline-block;background:rgba(184,149,106,0.15);border:1px solid var(--accent);color:var(--accent-bright);padding:0.3rem 0.8rem;border-radius:15px;font-size:0.8rem;}

/* === چک‌لیست === */
.checklist-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;margin-top:2rem;}
.checklist-item{display:flex;align-items:center;gap:1rem;background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;transition:all 0.3s;cursor:pointer;user-select:none;}
.checklist-item:hover{border-color:var(--accent);}
.checklist-item.checked{background:rgba(184,149,106,0.1);border-color:var(--accent);}
.checklist-box{width:22px;height:22px;border:2px solid var(--border);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:1rem;color:transparent;transition:all 0.3s;flex-shrink:0;}
.checklist-item.checked .checklist-box{background:var(--accent);border-color:var(--accent);color:var(--bg-dark);}
.checklist-label{color:var(--text-secondary);font-size:0.95rem;direction:ltr;}
.checklist-item.checked .checklist-label{color:var(--accent-bright);}
.progress-bar{max-width:600px;margin:2rem auto;background:var(--bg-card);border:1px solid var(--border);border-radius:50px;height:30px;overflow:hidden;position:relative;}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--accent) 0%,var(--accent-bright) 100%);width:0%;transition:width 0.5s ease;box-shadow:0 0 20px var(--accent-glow);}
.progress-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:var(--bg-dark);font-weight:700;font-size:0.9rem;z-index:1;}

/* === کارت شوالیه در صفحه‌ی اصلی === */
.knight-preview{display:flex;gap:3rem;align-items:center;background:linear-gradient(135deg,rgba(184,149,106,0.15) 0%,rgba(106,74,154,0.15) 100%);border:1px solid var(--border);border-radius:20px;padding:3rem;margin-top:2rem;flex-wrap:wrap;transition:all 0.3s;}
.knight-preview:hover{border-color:var(--accent);box-shadow:0 20px 50px rgba(0,0,0,0.5),0 0 40px var(--accent-glow);}
.knight-preview-image{width:220px;height:220px;border-radius:16px;background:radial-gradient(circle at center,#1e1e2a 0%,#0e0e15 100%);border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;padding:1rem;flex-shrink:0;}
.knight-preview-image img{max-width:100%;max-height:100%;object-fit:contain;filter:drop-shadow(0 0 15px rgba(184,149,106,0.4));}
.knight-preview-info{flex:1;min-width:250px;}
.knight-preview-title{font-size:2.5rem;color:var(--accent);margin-bottom:0.5rem;}
.knight-preview-desc{color:var(--text-secondary);font-size:1.05rem;line-height:2;margin-bottom:1.5rem;}

.download-card{display:flex;gap:3rem;background:var(--bg-card);padding:3rem;border-radius:14px;border:1px solid var(--border);align-items:center;flex-wrap:wrap;}
.game-cover{width:280px;height:280px;border-radius:12px;border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at center,#2a2a3a 0%,#0a0a0f 100%);font-size:6rem;color:var(--accent);}
.download-info{flex:1;min-width:280px;}
.download-info h2{color:var(--accent);margin-bottom:1rem;font-size:1.8rem;}
.download-info p{color:var(--text-secondary);margin-bottom:1rem;}
.download-details{list-style:none;margin:1.5rem 0;padding:1.5rem;background:var(--bg-dark);border-radius:10px;border:1px solid var(--border);}
.download-details li{padding:0.5rem 0;color:var(--text-secondary);}
.about-card{max-width:600px;margin:0 auto;background:var(--bg-card);padding:3rem;border-radius:14px;border:1px solid var(--border);text-align:center;}
.about-avatar{width:150px;height:150px;border-radius:50%;border:4px solid var(--accent);margin:0 auto 1.5rem;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at center,#2a2a3a 0%,#0a0a0f 100%);font-size:4rem;color:var(--accent);}
.about-card h2{color:var(--accent);font-size:2rem;margin-bottom:0.5rem;}
.about-role{color:var(--text-secondary);margin-bottom:1.5rem;}
.about-contact{background:var(--bg-dark);padding:1rem;border-radius:10px;margin-bottom:1.5rem;border:1px solid var(--border);}
.about-contact a{color:var(--accent);text-decoration:none;}
.about-desc{color:var(--text-secondary);line-height:2;}
.footer{background:var(--bg-card);border-top:1px solid var(--border);padding:4rem 2rem;text-align:center;margin-top:4rem;position:relative;z-index:1;}
.profile-card{display:flex;align-items:center;justify-content:center;gap:2rem;margin-bottom:2rem;flex-wrap:wrap;}
.profile-avatar{width:100px;height:100px;border-radius:50%;border:3px solid var(--accent);display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at center,#2a2a3a 0%,#0a0a0f 100%);font-size:2.5rem;color:var(--accent);}
.profile-info h3{color:var(--accent);font-size:1.3rem;margin-bottom:0.3rem;}
.profile-info p{color:var(--text-secondary);}
.profile-info a{color:var(--accent-bright);text-decoration:none;}
.copyright{color:var(--text-secondary);font-size:0.9rem;}
.back-to-top{position:fixed;bottom:2rem;left:2rem;width:50px;height:50px;border-radius:50%;background:var(--accent);color:var(--bg-dark);border:none;font-size:1.5rem;cursor:pointer;display:none;align-items:center;justify-content:center;box-shadow:0 0 20px var(--accent-glow);z-index:100;font-family:inherit;}
.back-to-top.show{display:flex;}
@media (max-width:768px){
.navbar{padding:1rem 1.5rem;}
.hamburger{display:block;}
.nav-links{display:none;width:100%;flex-direction:column;gap:0.8rem;padding-top:1rem;text-align:center;}
.nav-links.open{display:flex;}
.section{padding:3rem 1.5rem;}
.hero-title{font-size:3rem;}
.boss-header{flex-direction:column;text-align:center;}
.boss-meta{justify-content:center;}
.boss-title-fa{font-size:2rem;}
.profile-card{flex-direction:column;}
.story-content{padding:1.5rem;}
.download-card{padding:1.5rem;}
.lore-header{flex-direction:column;text-align:center;}
.knight-hero{flex-direction:column;text-align:center;padding:2rem;}
.knight-hero-title{font-size:2.5rem;}
.knight-preview{flex-direction:column;text-align:center;padding:2rem;}
.journey-timeline{padding-right:2rem;}
}
"""


def page(title, content):
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='45' fill='%230a0a0f' stroke='%23b8956a' stroke-width='4'/%3E%3Cpath d='M 30 45 Q 50 25 70 45 Q 70 70 50 80 Q 30 70 30 45 Z' fill='%23b8956a'/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div id="particles"></div>
<nav class="navbar">
<div class="nav-brand"><span class="brand-icon">✦</span><span>Hollow Knight</span></div>
<button class="hamburger" onclick="document.getElementById('navLinks').classList.toggle('open')">☰</button>
<ul class="nav-links" id="navLinks">
<li><a href="/">خانه</a></li>
<li><a href="/#bosses">باس‌ها</a></li>
<li><a href="/story">داستان</a></li>
<li><a href="/lore">تاریخ</a></li>
<li><a href="/knight">🛡️ شوالیه</a></li>
<li><a href="/map">نقشه</a></li>
<li><a href="/history">درباره بازی</a></li>
<li><a href="/download">دانلود</a></li>
<li><a href="/about">سازنده</a></li>
</ul>
</nav>
<main>{content}</main>
<button class="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<footer class="footer">
<div class="profile-card">
<div class="profile-avatar">🎮</div>
<div class="profile-info">
<h3>{CREATOR_NAME}</h3>
<p>شماره تماس: <a href="tel:{CREATOR_PHONE}" dir="ltr">{CREATOR_PHONE}</a></p>
</div>
</div>
<p class="copyright">ساخته شده با ❤️ برای جامعه‌ی Hollow Knight</p>
</footer>
<script>
window.addEventListener('scroll',function(){{
var btn=document.querySelector('.back-to-top');
if(window.scrollY>500){{btn.classList.add('show');}}else{{btn.classList.remove('show');}}
}});
(function(){{
var c=document.getElementById('particles');
for(var i=0;i<30;i++){{
var p=document.createElement('div');
p.className='particle';
var s=Math.random()*3+1;
p.style.width=s+'px';p.style.height=s+'px';
p.style.left=Math.random()*100+'%';
p.style.top=Math.random()*100+'%';
p.style.animationDuration=(Math.random()*20+15)+'s';
p.style.animationDelay=(Math.random()*10)+'s';
c.appendChild(p);
}}
}})();
</script>
</body>
</html>'''


@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory("images", filename)


@app.route("/map/<filename>")
def serve_map(filename):
    return send_from_directory("map", filename)


@app.route("/characters/<filename>")
def serve_character(filename):
    return send_from_directory("characters", filename)


# ⬅️ جدید: route برای سرو کردن عکس‌های شوالیه
@app.route("/knight/<filename>")
def serve_knight(filename):
    return send_from_directory("knight", filename)


@app.route("/")
def index():
    cards = ""
    for b in BOSSES:
        svg = boss_image_html(b["id"], b["name_en"])
        diff = DIFFICULTY.get(b["id"], 3)
        cards += f'''<a href="/boss/{b["id"]}" class="boss-card" data-name-fa="{b["name_fa"]}" data-name-en="{b["name_en"]}" data-location="{b["location_fa"]}">
<div class="boss-card-image">{svg}</div>
<div class="boss-card-content">
<h3 class="boss-name-fa">{b["name_fa"]}</h3>
<p class="boss-name-en">{b["name_en"]}</p>
<p class="boss-location">📍 {b["location_fa"]}</p>
<p style="font-size:0.9rem;letter-spacing:2px;">{stars_html(diff)}</p>
</div></a>'''

    filters_html = ""
    for loc_id, loc_name in LOCATIONS:
        active = " active" if loc_id == "all" else ""
        filters_html += f'<button class="filter-btn{active}" onclick="filterByLocation(\'{loc_id}\',this)">{loc_name}</button>'

    # ⬅️ جدید: کارت شوالیه برای صفحه‌ی اصلی
    knight_img_file = find_image("knight", "knight")
    if knight_img_file:
        knight_preview_img = f'<img src="/knight/{knight_img_file}" alt="The Knight">'
    else:
        knight_preview_img = '<div style="font-size:5rem;">🛡️</div>'

    content = f'''<section class="hero">
<div>
<h1 class="hero-title">هالوونست</h1>
<p class="hero-subtitle">پادشاهی‌ای که در سایه‌ی عفونت فراموش شد</p>
<div class="hero-buttons">
<a href="#bosses" class="btn-primary">مشاهده‌ی باس‌ها</a>
<a href="/lore" class="btn-secondary">تاریخ هالوونست</a>
</div>
</div>
</section>

<!-- ⬅️ جدید: بخش شوالیه در صفحه‌ی اصلی -->
<section class="section">
<h2 class="section-title">🛡️ شوالیه</h2>
<div class="knight-preview">
<div class="knight-preview-image">{knight_preview_img}</div>
<div class="knight-preview-info">
<h3 class="knight-preview-title">The Knight</h3>
<p class="knight-preview-desc">ظرفی از وُید که برای نابودی رادیانس خلق شد. سفری طولانی از پرتگاه تا معبد تخم سیاه، برای آزادسازی هالوونست از نفرین عفونت.</p>
<a href="/knight" class="btn-primary">مشاهده‌ی پروفایل کامل شوالیه</a>
</div>
</div>
</section>

<section id="story" class="section">
<h2 class="section-title">داستان بازی</h2>
<div class="story-content"><p>{GAME_STORY[:600]}...</p></div>
<div class="center-btn"><a href="/story" class="btn-secondary">ادامه‌ی داستان</a></div>
</section>

<section id="bosses" class="section">
<h2 class="section-title">باس‌های هالوونست</h2>
<div class="search-bar"><input type="text" id="searchInput" placeholder="جستجوی باس..." onkeyup="filterBosses()"></div>
<div class="filter-bar">{filters_html}</div>
<div class="bosses-grid" id="bossesGrid">{cards}</div>
<p class="no-results" id="noResults">باسی با این مشخصات پیدا نشد 😕</p>
</section>

<script>
function filterBosses(){{
var q=document.getElementById('searchInput').value.toLowerCase().trim();
var cards=document.querySelectorAll('.boss-card');
var v=0;
cards.forEach(function(c){{
var fa=c.getAttribute('data-name-fa').toLowerCase();
var en=c.getAttribute('data-name-en').toLowerCase();
if(fa.includes(q)||en.includes(q)||q===''){{c.style.display='flex';v++;}}else{{c.style.display='none';}}
}});
document.getElementById('noResults').style.display=v===0?'block':'none';
}}
function filterByLocation(loc,btn){{
document.querySelectorAll('.filter-btn').forEach(function(b){{b.classList.remove('active');}});
btn.classList.add('active');
var cards=document.querySelectorAll('.boss-card');
var v=0;
cards.forEach(function(c){{
var l=c.getAttribute('data-location');
if(loc==='all'||l.includes(loc)){{c.style.display='flex';v++;}}else{{c.style.display='none';}}
}});
document.getElementById('noResults').style.display=v===0?'block':'none';
}}
</script>'''
    return page("Hollow Knight | دانش‌نامه‌ی هالوونست", content)


# ⬅️ جدید: صفحه‌ی اختصاصی شوالیه
@app.route("/knight")
def knight_page():
    # گالری عکس‌ها
    knight_images = get_knight_images()
    gallery_html = ""
    if knight_images:
        for i, img in enumerate(knight_images):
            captions = ["شوالیه", "شوالیه با شنل", "شوالیه با شمشیر", "پرواز در تاریکی", "شوالیه در پرتگاه"]
            cap = captions[i] if i < len(captions) else f"تصویر {i+1}"
            gallery_html += f'''<div class="gallery-item" onclick="openLightbox('/knight/{img}')">
<img src="/knight/{img}" alt="{cap}">
<div class="gallery-caption">{cap}</div>
</div>'''
    else:
        gallery_html = '<p style="color:var(--text-secondary);text-align:center;">عکسی در پوشه‌ی knight پیدا نشد.</p>'

    # تصویر اصلی
    main_img_file = find_image("knight", "knight")
    if not main_img_file and knight_images:
        main_img_file = knight_images[0]
    if main_img_file:
        main_img_html = f'<img src="/knight/{main_img_file}" alt="The Knight">'
    else:
        main_img_html = '<div style="font-size:6rem;">🛡️</div>'

    # توانایی‌ها
    abilities_html = ""
    for a in KNIGHT_ABILITIES:
        abilities_html += f'''<div class="ability-card">
<span class="ability-icon">{a["icon"]}</span>
<h3 class="ability-name-fa">{a["name_fa"]}</h3>
<p class="ability-name-en">{a["name_en"]}</p>
<p class="ability-desc">{a["desc"]}</p>
</div>'''

    # مسیر سفر
    journey_html = ""
    for j in KNIGHT_JOURNEY:
        journey_html += f'''<div class="journey-item">
<div class="journey-card">
<span class="journey-icon">{j["icon"]}</span>
<h3 class="journey-region-fa">{j["region_fa"]}</h3>
<p class="journey-region-en">{j["region"]}</p>
<p class="journey-desc">{j["desc"]}</p>
</div>
</div>'''

    # پایان‌ها
    endings_html = ""
    for e in KNIGHT_ENDINGS:
        endings_html += f'''<div class="ending-card">
<span class="ending-icon">{e["icon"]}</span>
<h3 class="ending-name-fa">{e["name_fa"]}</h3>
<p class="ending-name-en">{e["name_en"]}</p>
<p class="ending-desc">{e["desc"]}</p>
<span class="ending-req">شرط: {e["requirement"]}</span>
</div>'''

    # چک‌لیست
    checklist_html = ""
    for item in KNIGHT_CHECKLIST:
        checklist_html += f'''<div class="checklist-item" onclick="toggleCheck(this)">
<div class="checklist-box">✓</div>
<span class="checklist-label">{item}</span>
</div>'''

    content = f'''<section class="section" style="padding-top:3rem;">
<!-- هدر شوالیه -->
<div class="knight-hero">
<div class="knight-hero-image">{main_img_html}</div>
<div class="knight-hero-info">
<h1 class="knight-hero-title">شوالیه</h1>
<p class="knight-hero-subtitle">The Knight — Ghost of Hallownest</p>
<p style="color:var(--text-secondary);line-height:2;margin-bottom:1rem;">
ظرفی از وُید که برای نابودی رادیانس خلق شد. بی‌نام، بی‌چهره، بی‌احساس.
</p>
<div class="knight-hero-tags">
<span class="knight-tag">🖤 Vessel</span>
<span class="knight-tag">⚔️ Nail Wielder</span>
<span class="knight-tag">🌙 Dream Traveler</span>
<span class="knight-tag">✨ Void Given Focus</span>
</div>
</div>
</div>

<!-- گالری -->
<h2 class="section-title">📸 گالری تصاویر</h2>
<div class="knight-gallery">{gallery_html}</div>

<!-- داستان -->
<h2 class="section-title" style="margin-top:5rem;">📖 داستان شوالیه</h2>
<div class="story-content"><p>{KNIGHT_STORY}</p></div>

<!-- توانایی‌ها -->
<h2 class="section-title" style="margin-top:5rem;">⚔️ توانایی‌ها و تجهیزات</h2>
<div class="abilities-grid">{abilities_html}</div>

<!-- مسیر سفر -->
<h2 class="section-title" style="margin-top:5rem;">🗺️ مسیر سفر شوالیه</h2>
<div class="journey-timeline">{journey_html}</div>

<!-- پایان‌ها -->
<h2 class="section-title" style="margin-top:5rem;">🎬 پایان‌های بازی</h2>
<div class="endings-grid">{endings_html}</div>

<!-- چک‌لیست -->
<h2 class="section-title" style="margin-top:5rem;">✅ چک‌لیست پیشرفت</h2>
<p style="text-align:center;color:var(--text-secondary);max-width:700px;margin:0 auto 2rem;">
روی هر توانایی که به دست آوردی کلیک کن تا پیشرفتت ثبت شود.
</p>
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div><span class="progress-text" id="progressText">0%</span></div>
<div class="checklist-grid">{checklist_html}</div>

<!-- لایت‌باکس -->
<div id="lightbox" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.95);z-index:1000;align-items:center;justify-content:center;cursor:pointer;" onclick="this.style.display='none'">
<img id="lightboxImg" style="max-width:90%;max-height:90%;border:2px solid var(--accent);border-radius:12px;" src="">
</div>

<div class="center-btn" style="margin-top:4rem;"><a href="/" class="btn-secondary">← بازگشت به خانه</a></div>
</section>

<script>
function openLightbox(src){{
document.getElementById('lightboxImg').src = src;
document.getElementById('lightbox').style.display = 'flex';
}}

function toggleCheck(el){{
el.classList.toggle('checked');
updateProgress();
}}

function updateProgress(){{
var total = document.querySelectorAll('.checklist-item').length;
var checked = document.querySelectorAll('.checklist-item.checked').length;
var pct = total > 0 ? Math.round((checked / total) * 100) : 0;
document.getElementById('progressFill').style.width = pct + '%';
document.getElementById('progressText').textContent = pct + '%';
}}

// بارگذاری وضعیت از localStorage
document.addEventListener('DOMContentLoaded', function(){{
var items = document.querySelectorAll('.checklist-item');
items.forEach(function(item, i){{
var saved = localStorage.getItem('knight_check_' + i);
if(saved === 'true'){{ item.classList.add('checked'); }}
item.addEventListener('click', function(){{
localStorage.setItem('knight_check_' + i, item.classList.contains('checked'));
}});
}});
updateProgress();
}});
</script>'''
    return page("شوالیه | Hollow Knight", content)


@app.route("/boss/<boss_id>")
def boss_detail(boss_id):
    boss = next((b for b in BOSSES if b["id"] == boss_id), None)
    if not boss:
        abort(404)
    svg = boss_image_html(boss["id"], boss["name_en"])
    diff = DIFFICULTY.get(boss["id"], 3)
    attacks = ""
    for a in boss["attacks"]:
        attacks += f'<li class="attack-item"><strong>{a["name"]}:</strong> {a["desc"]}</li>'

    dream_section = ""
    if boss.get("dream_version"):
        dream_section = f'''<div class="dream-section">
<h2>🌙 نسخه‌ی رؤیایی</h2>
<p>{boss["dream_version"]}</p>
</div>'''

    content = f'''<section class="section boss-detail">
<div class="boss-header">
<div class="boss-image-large">{svg}</div>
<div>
<h1 class="boss-title-fa">{boss["name_fa"]}</h1>
<p class="boss-title-en">{boss["name_en"]}</p>
<div class="boss-meta">
<span class="meta-item">📍 {boss["location_fa"]}</span>
<span class="meta-item">❤️ {boss["hp"]} HP</span>
<span class="meta-item">⚔️ سختی: {diff}/5</span>
</div>
</div>
</div>
{dream_section}
<div class="boss-section"><h2>⚔️ انواع حملات</h2><ul class="attacks-list">{attacks}</ul></div>
<div class="boss-section"><h2>🔑 پیش‌نیازها</h2><p>{boss["prerequisites_fa"]}</p></div>
<div class="boss-section"><h2>🏆 بهترین استراتژی نبرد</h2><p>{boss["strategy_fa"]}</p></div>
<div class="boss-section"><h2>📖 داستان</h2><p>{boss["story_fa"]}</p></div>
<div class="boss-section">
<h2>🎬 ویدئوی فایت</h2>
<div class="video-wrapper"><iframe src="{APARAT_VIDEO}" allowfullscreen></iframe></div>
</div>
<a href="/" class="btn-secondary">← بازگشت</a>
</section>'''
    return page(f'{boss["name_fa"]} | Hollow Knight', content)


@app.route("/lore")
def lore():
    sections_html = ""
    for c in CHARACTERS:
        img_html = character_image_html(c["id"], c["name_en"])
        sections_html += f'''<div class="lore-section">
<div class="lore-header">
<div class="lore-image">{img_html}</div>
<div class="lore-info">
<h2 class="lore-title-fa">{c["name_fa"]}</h2>
<p class="lore-title-en">{c["name_en"]}</p>
<span class="lore-type">{c["type_fa"]}</span>
</div>
</div>
<div class="lore-text">{c["story_fa"]}</div>
</div>'''

    content = f'''<section class="section">
<h1 class="section-title">📜 تاریخ و افسانه‌های هالوونست</h1>
<p style="text-align:center;color:var(--text-secondary);max-width:800px;margin:0 auto 3rem;font-size:1.1rem;line-height:2;">
در این بخش، با مهم‌ترین مکان‌ها، شخصیت‌ها و افسانه‌های هالوونست آشنا می‌شوید. از معبد تخم سیاه تا پادشاه رنگ‌پریده، از رویابین‌ها تا همراهان وفادار.
</p>
{sections_html}
<div class="center-btn"><a href="/" class="btn-secondary">← بازگشت</a></div>
</section>'''
    return page("تاریخ و افسانه‌ها | Hollow Knight", content)


@app.route("/story")
def story():
    content = f'''<section class="section">
<h1 class="section-title">داستان کامل هالوونست</h1>
<div class="boss-section">
<h2>🎬 ویدئوی خلاصه‌ی داستان</h2>
<div class="video-wrapper"><iframe src="{STORY_VIDEO}" allowfullscreen></iframe></div>
</div>
<div class="story-content"><p>{GAME_STORY}</p></div>
<div class="center-btn"><a href="/" class="btn-secondary">← بازگشت</a></div>
</section>'''
    return page("داستان | Hollow Knight", content)


@app.route("/map")
def map_page():
    map_file = find_map_image()
    if map_file:
        map_html = f'<div class="map-container"><img src="/map/{map_file}" alt="نقشه‌ی هالوونست"></div>'
    else:
        map_html = '<p style="text-align:center;color:#9a9a9a;">فایل نقشه یافت نشد</p>'

    regions = [
        "گذرگاه فراموش‌شده", "مسیر سبز", "زباله‌های قارچی", "شهر اشک‌ها",
        "آبراه‌های سلطنتی", "قله‌ی کریستال", "تودرتوی عمیق", "باغ‌های ملکه",
        "کولوسئوم احمق‌ها", "کندو", "چادر گریم", "Pantheon of Hallownest",
        "معبد تخم سیاه", "Dirtmouth", "Deepnest", "Howling Cliffs",
        "The Hive", "Kingdom's Edge", "Ancient Basin", "Fog Canyon",
    ]
    regions_html = ""
    for r in regions:
        regions_html += f'<div class="region-card">📍 {r}</div>'

    content = f'''<section class="section">
<h1 class="section-title">نقشه‌ی هالوونست</h1>
{map_html}
<h2 class="section-title" style="margin-top:4rem;">مناطق هالوونست</h2>
<div class="regions-grid">{regions_html}</div>
<div class="center-btn"><a href="/" class="btn-secondary">← بازگشت</a></div>
</section>'''
    return page("نقشه | Hollow Knight", content)


@app.route("/history")
def history():
    content = f'''<section class="section">
<h1 class="section-title">درباره‌ی بازی Hollow Knight</h1>
<div class="story-content"><p>{GAME_HISTORY}</p></div>
<div class="center-btn"><a href="/" class="btn-secondary">← بازگشت</a></div>
</section>'''
    return page("درباره بازی | Hollow Knight", content)


@app.route("/download")
def download():
    content = f'''<section class="section">
<h1 class="section-title">دانلود بازی Hollow Knight</h1>
<div class="download-card">
<div class="game-cover">🎮</div>
<div class="download-info">
<h2>Hollow Knight - نسخه‌ی کامل</h2>
<p>شامل تمام DLCها: Hidden Dreams, The Grimm Troupe, Lifeblood, Godmaster</p>
<ul class="download-details">
<li>📦 فرمت: RAR</li>
<li>💾 حجم: حدود ۱ گیگابایت</li>
<li>🖥️ پلتفرم: PC (Windows)</li>
<li>🌐 زبان: انگلیسی</li>
</ul>
<a href="{GAME_DOWNLOAD_URL}" class="btn-primary" target="_blank" rel="noopener">⬇️ دانلود مستقیم</a>
</div>
</div>
</section>'''
    return page("دانلود | Hollow Knight", content)


@app.route("/about")
def about():
    content = f'''<section class="section">
<h1 class="section-title">درباره‌ی سازنده</h1>
<div class="about-card">
<div class="about-avatar">🎮</div>
<h2>{CREATOR_NAME}</h2>
<p class="about-role">طراح و توسعه‌دهنده‌ی سایت</p>
<p class="about-contact">📞 شماره تماس: <a href="tel:{CREATOR_PHONE}" dir="ltr">{CREATOR_PHONE}</a></p>
<p class="about-desc">این سایت به‌عنوان یک پروژه‌ی شخصی برای علاقه‌مندان به بازی Hollow Knight طراحی شده است.</p>
</div>
</section>'''
    return page("سازنده | Hollow Knight", content)


@app.route("/debug")
def debug_files():
    def list_dir(path):
        if not os.path.exists(path):
            return f"<p>پوشه‌ی <code>{path}</code> وجود ندارد.</p>"
        files = os.listdir(path)
        if not files:
            return f"<p>پوشه‌ی <code>{path}</code> خالی است.</p>"
        html = f"<h3>پوشه‌ی {path}</h3><ul>"
        for f in files:
            is_img = "✅ تصویر" if is_image(f) else "❌ غیرتصویری"
            clean = clean_filename(f)
            html += f"<li><code>{f}</code> → نام پاک‌شده: <code>{clean}</code> ({is_img})</li>"
        html += "</ul>"
        return html

    content = f'''<section class="section">
<h1 class="section-title">🐛 دیباگ فایل‌ها</h1>
<div class="story-content" style="direction:ltr;text-align:left;">
{list_dir("images")}
{list_dir("characters")}
{list_dir("knight")}
{list_dir("map")}
</div>
<div class="center-btn"><a href="/" class="btn-secondary">← بازگشت</a></div>
</section>'''
    return page("دیباگ | Hollow Knight", content)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎮 سایت Hollow Knight در حال اجراست!")
    print("="*50)
    print(f"👤 سازنده: {CREATOR_NAME}")
    print(f"📞 شماره: {CREATOR_PHONE}")
    print(f"🌐 آدرس: http://127.0.0.1:5000")
    print(f"🛡️ صفحه‌ی شوالیه: http://127.0.0.1:5000/knight")
    print(f"🐛 دیباگ: http://127.0.0.1:5000/debug")
    print(f"📊 تعداد باس‌ها: {len(BOSSES)}")
    print(f"📜 تعداد کاراکترها: {len(CHARACTERS)}")
    print("="*50 + "\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)