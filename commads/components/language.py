class Language:
    def __init__(self):
        self.visual_qr_reply = ["Generate Visual QR 🌉", "Genera QR Visivo 🌉", "विजुअल क्यूआर बनाएं 🌉", "Generar QR Visual 🌉", "Générer un QR Visuel 🌉", "Generiere visuellen QR 🌉", "Создать визуальный QR 🌉", "Створити візуальний QR 🌉", "生成视觉 QR 🌉", "إنشاء رمز الاستجابة السريعة المرئي 🌉"]
        self.normal_qr_reply = ["Generate Normal QRcode 🌱", "Genera QRcode Normale 🌱", "सामान्य QRकोड बनाएं 🌱", "Generar Código QR Normal 🌱", "Générer un QRcode Normal 🌱", "Generiere normalen QRcode 🌱", "Создать обычный QR-код 🌱", "Створити звичайний QR-код 🌱", "生成普通 QR 码 🌱", "إنشاء رمز الاستجابة السريعة العادي 🌱"]
        self.custom_background_reply = ["Custom Background 🔥", "Sfondo Personalizzato 🔥", "कस्टम पृष्ठभूमि 🔥", "Fondo Personalizado 🔥", "Benutzerdefinierter Hintergrund 🔥", "Индивидуальный фон 🔥", "Індивідуальний фон 🔥"]
        self.custom_foreground_reply = ["Custom Foreground", "Personalizza Primo Piano", "कस्टम पहला प्लान", "Primer plano personalizado", "Arrière-plan Personnalisé", "Benutzerdefinierter Vordergrund", "Индивидуальный передний план", "Індивідуальний передній план", "自定义前景", "الخلفية المخصصة"]
        self.previus_color_reply = ["previous color 🎨", "colore precedente 🎨", "पिछला रंग 🎨", "color anterior 🎨", "couleur précédente 🎨", "vorherige Farbe 🎨", "предыдущий цвет 🎨", "попередній колір 🎨", "上一种颜色 🎨", "اختر اللون 🎨", "اللون السابق 🎨"]
        self.language_setting_reply = ["Language setting 🇬🇧", "Impostazioni Lingua 🇮🇹", "भाषा सेटिंग 🇮🇳", "Configuración de Idioma 🇪🇸", "Paramètres de Langue 🇫🇷", "Spracheinstellungen 🇩🇪", "Настройки Языка 🇷🇺", "Налаштування Мови 🇺🇦", "语言设置 🇨🇳", "إعداد اللغة 🇸🇦"]
        self.create_qr_ai = ["AI Qrcode 🤖", "Codice QR AI 🤖", "एआई क्यूआरकोड 🤖", "Código QR de IA 🤖", "KI-Qrcode 🤖", "QR code IA 🤖", "QR-код ИИ 🤖", "Налаштування Мови 🇺🇦", "QR-код ШІ 🤖", "AI 二维码 🤖", "رمز الاستجابة السريعة الذكاء الصناعي 🤖"]
        self.version = ["Version"]
        self.advanced = ["Advanced"]
        self.back_to_custom = ["Back 🔙", "Indietro 🔙", "वापस 🔙", "Volver 🔙", "Retour 🔙", "Zurück 🔙", "Назад 🔙", "Назад 🔙", "Назад 🔙", "返回 🔙", "العودة 🔙"]
        self.cancel_operation = ["Cancel ❌", "Annulla ❌", "रद्द करें ❌", "Cancelar ❌", "Annuler ❌", "Abbrechen ❌", "Отмена ❌", "Відмінити ❌", "取消 ❌", "إلغاء ❌"]
        
    def start_lang(self, first_name, language_code):
        tutorial_link = '<a href="https://telegra.ph/TUTORIAL-QR-BOT-05-05">tutorial</a>' 
        ads_plicy_link = '<a href="https://telegra.ph/Ads-Policy-05-05">Ads policy</a>'
        privacy_policy_link = '<a href="https://telegra.ph/Privacy-Policy-05-05-46">Privacy policy</a>'
        channel_link = '<a href="https://t.me/tasu_Channel">👇</a>'
        eng = ( f"Hello {first_name} 👋 , Welcome! \n"
            "📸 You can send me an image of a QR code or a Barcode and I will scan it for you. \n"
            "\n"
            "🎨 Customize your QR code (Visual QR 🌉)\n"
            "🔥 New AI Remove Background function available!\n"
            "\n"
            "⚠️ However, keep in mind that I can scan many types of Barcodes, but not all.\n"
            "You can view the short tutorial and other curiosity in my channel!\n"
            f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}")     
        lang_text = {
            'it': (f"Ciao {first_name} 👋 , benvenuto! \n"
                "📸 Puoi inviarmi l'immagine di un codice QR o un codice a barre e lo scansionerò per te. \n"
                "\n"
                "🎨 Personalizza il tuo codice QR (Visual QR 🌉)\n"
                "🔥 Nuova funzione AI Remove Background disponibile!\n"
                "\n"
                "⚠️ Tuttavia, tieni presente che posso scansionare molti tipi di codici a barre, ma non tutti.\n"
                "Potete vedere il breve tutorial e altre curiosità nel mio canale!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'en': eng,
            'hi': (f"नमस्ते {first_name} 👋 , स्वागत है! \n"
                "📸 आप मुझे कोड या बारकोड की एक छवि भेज सकते हैं, और मैं आपके लिए इसे स्कैन करूँगा। \n"
                "\n"
                "🎨 अपने क्यूआर कोड को अनुकूलित करें (विजुअल क्यूआर 🌉)\n"
                "🔥 नई ए.आई. हटाएं पृष्ठभूमि कार्यक्षमता उपलब्ध है!\n"
                "\n"
                "⚠️ हालांकि, ध्यान रखें कि मैं कई प्रकार के बारकोड को स्कैन कर सकता हूँ, लेकिन सभी नहीं।\n"
                "आप मेरे चैनल में छोटे से ट्यूटोरियल और अन्य रोचक देख सकते हैं!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'es': (f"Hola {first_name} 👋 , ¡Bienvenido! \n"
                "📸 Puedes enviarme una imagen de un código QR o un Código de Barras y yo lo escanearé por ti. \n"
                "\n"
                "🎨 Personaliza tu código QR (Visual QR 🌉)\n"
                "🔥 ¡Nueva función AI Eliminar Fondo disponible!\n"
                "\n"
                "⚠️ Sin embargo, ten en cuenta que puedo escanear muchos tipos de Códigos de Barras, pero no todos.\n"
                "¡Puedes ver el breve tutorial y otras curiosidades en mi canal!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'fr': (f"Bonjour {first_name} 👋 , Bienvenue! \n"
                "📸 Vous pouvez m'envoyer une image d'un code QR ou d'un code-barres et je le scannerai pour vous. \n"
                "\n"
                "🎨 Personnalisez votre code QR (QR visuel 🌉)\n"
                "🔥 Nouvelle fonction AI Supprimer l'arrière-plan disponible!\n"
                "\n"
                "⚠️ Cependant, gardez à l'esprit que je peux scanner plusieurs types de codes-barres, mais pas tous.\n"
                "Vous pouvez consulter le court tutoriel et d'autres curiosités sur ma chaîne !\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'de': (f"Hallo {first_name} 👋 , Willkommen! \n"
                "📸 Sie können mir ein Bild eines QR-Codes oder eines Barcodes senden, und ich werde es für Sie scannen. \n"
                "\n"
                "🎨 Passen Sie Ihren QR-Code an (Visueller QR 🌉)\n"
                "🔥 Neue AI Entfernen Sie die Hintergrundfunktion!\n"
                "\n"
                "⚠️ Beachten Sie jedoch, dass ich viele Arten von Barcodes scannen kann, aber nicht alle.\n"
                "Sie können das kurze Tutorial und andere Neugier in meinem Kanal ansehen!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'ru': (f"Привет {first_name} 👋 , Добро пожаловать! \n"
                "📸 Вы можете отправить мне изображение QR-кода или штрих-кода, и я отсканирую его для вас. \n"
                "\n"
                "🎨 Настройте свой QR-код (визуальный QR 🌉)\n"
                "🔥 Доступна новая функция Исключить фон с помощью искусственного интеллекта!\n"
                "\n"
                "⚠️ Однако имейте в виду, что я могу сканировать многие типы штрих-кодов, но не все.\n"
                "Вы можете посмотреть короткое руководство и другие интересные материалы на моем канале!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'uk': (f"Привіт {first_name} 👋 , Ласкаво просимо! \n"
                "📸 Ви можете надіслати мені зображення QR-коду або штрих-коду, і я сканую його для вас. \n"
                "\n"
                "🎨 Налаштуйте свій QR-код (Візуальний QR 🌉)\n"
                "🔥 Доступна нова функція Штучний інтелект Видалити фон!\n"
                "\n"
                "⚠️ Однак майте на увазі, що я можу сканувати багато типів штрих-кодів, але не всі.\n"
                "Ви можете переглянути короткий урок та інші цікавинки на моєму каналі!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'zh': (f"你好 {first_name} 👋 , 欢迎! \n"
                "📸 您可以向我发送 QR 码或条形码的图像，我会为您扫描它。 \n"
                "\n"
                "🎨 自定义您的 QR 码 (可视化 QR 🌉)\n"
                "🔥 新的 AI 删除背景功能可用!\n"
                "\n"
                "⚠️ 但请注意，我可以扫描许多类型的条形码，但不是所有类型。\n"
                "您可以在我的频道中查看简短的教程和其他有趣的内容！\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
            'ar': (f"مرحبا {first_name} 👋 , مرحبًا! \n"
                "📸 يمكنك إرسال صورة لي لرمز الاستجابة السريعة أو رمز الباركود وسأقوم بمسحه لك. \n"
                "\n"
                "🎨 قم بتخصيص رمز الاستجابة السريعة الخاص بك (رمز الاستجابة السريعة المرئي 🌉)\n"
                "🔥 توفر وظيفة إزالة الخلفية الجديدة بالذكاء الاصطناعي!\n"
                "\n"
                "⚠️ ومع ذلك، يرجى ملاحظة أنه يمكنني مسح العديد من أنواع أكواد الباركود، ولكن ليس كلها.\n"
                "يمكنك مشاهدة البرنامج التعليمي القصير وغيرها من الاستفسارات في قناتي!\n"
                f"{channel_link}-{ads_plicy_link}-{privacy_policy_link}-{tutorial_link}"),
        }
        return lang_text.get(language_code, eng)
    
    def visual_qr(self, language_code):
        eng = "Generate Visual QR 🌉"
        lang_text = {
            'it': "Genera QR Visivo 🌉",
            'en': eng,
            'hi': "विजुअल क्यूआर बनाएं 🌉",
            'es': "Generar QR Visual 🌉",
            'fr': "Générer un QR Visuel 🌉",
            'de': "Generiere visuellen QR 🌉",
            'ru': "Создать визуальный QR 🌉",
            'uk': "Створити візуальний QR 🌉",
            'zh': "生成视觉 QR 🌉",
            'ar': "إنشاء رمز الاستجابة السريعة المرئي 🌉"
        }
        return lang_text.get(language_code, eng)
    
    def normal_qr(self, language_code):
        eng = "Generate Normal QRcode 🌱"
        lang_text = {
            'it': "Genera QRcode Normale 🌱",
            'en': eng,
            'hi': "सामान्य QRकोड बनाएं 🌱",
            'es': "Generar Código QR Normal 🌱",
            'fr': "Générer un QRcode Normal 🌱",
            'de': "Generiere normalen QRcode 🌱",
            'ru': "Создать обычный QR-код 🌱",
            'uk': "Створити звичайний QR-код 🌱",
            'zh': "生成普通 QR 码 🌱",
            'ar': "إنشاء رمز الاستجابة السريعة العادي 🌱"
        }
        return lang_text.get(language_code, eng)
    
    def scan_qr(self, language_code):
        eng = "Scan QR code 📸"
        lang_text = {
            'it': "Scansiona codice QR 📸",
            'en': eng,
            'hi': "क्यूआर कोड स्कैन करें 📸",
            'es': "Escanear código QR 📸",
            'fr': "Scanner le code QR 📸",
            'de': "QR-Code scannen 📸",
            'ru': "Сканировать QR-код 📸",
            'uk': "Сканувати QR-код 📸",
            'zh': "扫描 QR 码 📸",
            'ar': "مسح رمز الاستجابة السريعة 📸"
        }
        return lang_text.get(language_code, eng)

    def back(self, language_code):
        eng = "Back 🔙"
        lang_text = {
            'it': "Indietro 🔙",
            'en': eng,
            'hi': "पीछे 🔙",
            'es': "Volver 🔙",
            'fr': "Retour 🔙",
            'de': "Zurück 🔙",
            'ru': "Назад 🔙",
            'uk': "Назад 🔙",
            'zh': "返回 🔙",
            'ar': "العودة 🔙"
        }
        return lang_text.get(language_code, eng)
  
    def cancel(self, language_code):
        eng = "Cancel ❌"
        lang_text = {
            'it': "Annulla ❌",
            'en': eng,
            'hi': "रद्द करें ❌",
            'es': "Cancelar ❌",
            'fr': "Annuler ❌",
            'de': "Abbrechen ❌",
            'ru': "Отмена ❌",
            'uk': "Відмінити ❌",
            'zh': "取消 ❌",
            'ar': "إلغاء ❌"
        }
        return lang_text.get(language_code, eng)
    
    def send_text(self, language_code):
        eng = "Send me text 📝:"
        lang_text = {
            'it': "Inviami un testo 📝:",
            'en': eng,
            'hi': "मुझे एक टेक्स्ट भेजें 📝:",
            'es': "Envíame un texto 📝:",
            'fr': "Envoie-moi un texte 📝:",
            'de': "Sende mir einen Text 📝:",
            'ru': "Отправь мне текст 📝:",
            'uk': "Надішли мені текст 📝:",
            'zh': "发送文本 📝:",
            'ar': "أرسل لي نصاً 📝"
        }
        return lang_text.get(language_code, eng)
    
    def send_image(self, language_code):
        eng = "Send me Image 🌉 or gif 🎞:"
        lang_text = {
            'it': "Inviami un'immagine 🌉 o gif 🎞:",
            'en': eng,
            'hi': "मुझे एक छवि या gif भेजें 🌉🎞:",
            'es': "Envíame una imagen 🌉 o gif 🎞:",
            'fr': "Envoie-moi une image 🌉 ou un gif 🎞:",
            'de': "Sende mir ein Bild 🌉 oder ein gif 🎞:",
            'ru': "Отправь мне изображение 🌉 или gif 🎞:",
            'uk': "Надішли мені зображення 🌉 або gif 🎞:",
            'zh': "发送图片 🌉 或 gif 🎞：",
            'ar': "أرسل لي صورة 🌉 أو gif 🎞:"
        }
        return lang_text.get(language_code, eng)

    def waiting(self, language_code):
        eng = "Waiting..."
        lang_text = {
            'it': "In attesa...",
            'en': eng,
            'hi': "प्रतीक्षा कर रहा हूँ...",
            'es': "Esperando...",
            'fr': "En attente...",
            'de': "Warten...",
            'ru': "Ожидание...",
            'uk': "Очікування...",
            'zh': "等待中...",
            'ar': "في انتظار..."
        }
        return lang_text.get(language_code, eng)

    def error(self, language_code):
        eng = "Ops... an error has occurred 😔 contact owner or try again!"
        lang_text = {
            'it': "Ops... si è verificato un errore 😔 contatta il proprietario o riprova!",
            'en': eng,
            'hi': "ओह... कुछ गड़बड़ हो गई है 😔 मालिक से संपर्क करें या पुनः प्रयास करें!",
            'es': "Ops... ha ocurrido un error 😔 contacta al propietario o inténtalo de nuevo.",
            'fr': "Ops... une erreur s'est produite 😔 contactez le propriétaire ou réessayez !",
            'de': "Oops... ein Fehler ist aufgetreten 😔 kontaktiere den Besitzer oder versuche es erneut!",
            'ru': "Упс... произошла ошибка 😔 свяжитесь с владельцем или попробуйте снова!",
            'uk': "Ой... сталася помилка 😔 зверніться до власника або спробуйте ще раз!",
            'zh': "糟糕... 发生了错误 😔 联系所有者或重试!",
            'ar': "عذرًا... حدث خطأ 😔 اتصل بالمالك أو حاول مرة أخرى!"
        }
        return lang_text.get(language_code, eng)
    
    def file_not_valid(self, language_code):
        eng = "The image file is not valid 🚫"
        lang_text = {
            'it': "Il file dell'immagine non è valido 🚫",
            'en': eng,
            'hi': "चित्र फ़ाइल मान्य नहीं है 🚫",
            'es': "El archivo de imagen no es válido 🚫",
            'fr': "Le fichier image n'est pas valide 🚫",
            'de': "Die Bilddatei ist nicht gültig 🚫",
            'ru': "Файл изображения недопустим 🚫",
            'uk': "Файл зображення недійсний 🚫",
            'zh': "图像文件无效 🚫",
            'ar': "ملف الصورة غير صالح 🚫"
        }
        return lang_text.get(language_code, eng)

    def code_not_found(self, language_code):
        eng = "No code found or unable to decode it 🚫"
        lang_text = {
            'it': "Nessun codice trovato o impossibile decodificarlo 🚫",
            'en': eng,
            'hi': "कोई कोड नहीं मिला या इसे डिकोड करने में असमर्थ 🚫",
            'es': "No se encontró ningún código o no se puede decodificar 🚫",
            'fr': "Aucun code trouvé ou incapable de le décoder 🚫",
            'de': "Kein Code gefunden oder nicht entschlüsselbar 🚫",
            'ru': "Код не найден или не удается его декодировать 🚫",
            'uk': "Код не знайдено або не вдається його розкодувати 🚫",
            'zh': "未找到代码或无法解码 🚫",
            'ar': "لم يتم العثور على رمز أو عدم القدرة على فك تشفيره 🚫"
        }
        return lang_text.get(language_code, eng)

    def choose_color(self, language_code):
        eng = "Choose color 🎨"
        lang_text = {
            'it': "Scegli il colore 🎨",
            'en': eng,
            'hi': "रंग चुनें 🎨",
            'es': "Elige un color 🎨",
            'fr': "Choisissez la couleur 🎨",
            'de': "Farbe wählen 🎨",
            'ru': "Выберите цвет 🎨",
            'uk': "Виберіть колір 🎨",
            'zh': "选择颜色 🎨",
            'ar': "اختر اللون 🎨"
        }
        return lang_text.get(language_code, eng)

    def open_link(self, language_code):
        eng = "Open Link"
        lang_text = {
            'it': "Apri il link",
            'en': eng,
            'hi': "लिंक खोलें",
            'es': "Abrir enlace",
            'fr': "Ouvrir le lien",
            'de': "Link öffnen",
            'ru': "Открыть ссылку",
            'uk': "Відкрити посилання",
            'zh': "打开链接",
            'ar': "افتح الرابط"
        }
        return lang_text.get(language_code, eng)

    def confirm(self, language_code, qr):
        caption_status = '✅' if qr else '⚠️'
        eng = f"Confirm {caption_status}"
        lang_text = {
            'it': f"Conferma {caption_status}",
            'en': eng,
            'hi': f"पुष्टि {caption_status}",
            'es': f"Confirmar {caption_status}",
            'fr': f"Confirmer {caption_status}",
            'de': f"Bestätigen {caption_status}",
            'ru': f"Подтвердить {caption_status}",
            'uk': f"Підтвердити {caption_status}",
            'zh': f"确认 {caption_status}",
            'ar': f"تأكيد {caption_status}"
        }
        return lang_text.get(language_code, eng)

    def confirmed(self, language_code, qr):        
        eng = 'Readable ✅' if qr else 'Your qr is unreadable (internally)⚠️'
        lang_text = {
            'it': 'Leggibile ✅' if qr else 'Il tuo codice QR non è leggibile (internamente)⚠️',
            'en': eng,
            'hi': 'अधिपठनीय ✅' if qr else 'आपका क्यूआर अधिपठनीय नहीं है (आंतरिक रूप से)⚠️',
            'es': 'Legible ✅' if qr else 'Su código QR no es legible (internamente)⚠️',
            'fr': 'Lisible ✅' if qr else 'Votre QR code n\'est pas lisible (en interne)⚠️',
            'de': 'Lesbar ✅' if qr else 'Ihr QR-Code ist nicht lesbar (intern)⚠️',
            'ru': 'Читаемо ✅' if qr else 'Ваш QR-код нечитаем (внутренне)⚠️',
            'uk': 'Читабельний ✅' if qr else 'Ваш QR-код нечитабельний (внутрішньо)⚠️',
            'zh': '可读 ✅' if qr else '您的 QR 码无法读取（内部）⚠️',
            'ar': 'قابلة للقراءة ✅' if qr else 'لا يمكن قراءة رمز الاستجابة السريعة الخاص بك (داخليًا)⚠️'
        }
        return lang_text.get(language_code, eng)
    
    def rembg_mode(self, language_code):
        eng = "Choose the color (AI Remove Background Mode) 🤖:"
        lang_text = {
            'it': "Scegli il colore (Modalità Rimozione Sfondo con Intelligenza Artificiale) 🤖:",
            'en': eng,
            'hi': "रंग चुनें (ए.आई. हटाएं पृष्ठभूमि मोड) 🤖:",
            'es': "Elige el color (Modo de Eliminación de Fondo con Inteligencia Artificial) 🤖:",
            'fr': "Choisissez la couleur (Mode de suppression de l'arrière-plan avec l'IA) 🤖:",
            'de': "Wählen Sie die Farbe (KI-Entfernen des Hintergrunds-Modus) 🤖:",
            'ru': "Выберите цвет (Режим искусственного удаления фона) 🤖:",
            'uk': "Виберіть колір (Режим штучного видалення фону) 🤖:",
            'zh': "选择颜色（AI 移除背景模式）🤖：",
            'ar': "اختر اللون (وضع إزالة الخلفية بالذكاء الصناعي) 🤖:"
        }
        return lang_text.get(language_code, eng)

    def custom_foreground(self, language_code):
        eng = "Custom Foreground"
        lang_text = {
            'it': "Personalizza Primo Piano",
            'en': eng,
            'hi': "कस्टम पहला प्लान",
            'es': "Primer plano personalizado",
            'fr': "Avant-plan Personnalisé",
            'de': "Benutzerdefinierter Vordergrund",
            'ru': "Индивидуальный передний план",
            'uk': "Індивідуальний передній план",
            'zh': "自定义前景",
            'ar': "الخلفية المخصصة"
        }
        return lang_text.get(language_code, eng)

    def custom_background(self, language_code):
        eng = "Custom Background 🔥"
        lang_text = {
            'it': "Sfondo Personalizzato 🔥",
            'en': eng,
            'hi': "कस्टम पृष्ठभूमि 🔥",
            'es': "Fondo Personalizado 🔥",
            'fr': "Arrière-plan Personnalisé 🔥",
            'de': "Benutzerdefinierter Hintergrund 🔥",
            'ru': "Индивидуальный фон 🔥",
            'uk': "Індивідуальний фон 🔥",
            'zh': "自定义背景 🔥",
            'ar': "الخلفية المخصصة 🔥"
        }
        return lang_text.get(language_code, eng)
    
    def previous_color(self, language_code):
        eng = "previous color 🎨"
        lang_text = {
            'it': "colore precedente 🎨",
            'en': eng,
            'hi': "पिछला रंग 🎨",
            'es': "color anterior 🎨",
            'fr': "couleur précédente 🎨",
            'de': "vorherige Farbe 🎨",
            'ru': "предыдущий цвет 🎨",
            'uk': "попередній колір 🎨",
            'zh': "上一种颜色 🎨",
            'ar': "اللون السابق 🎨"
        }
        return lang_text.get(language_code, eng)
    
    def operation_deleted(self, language_code):
        eng = "operation deleted 🗑"
        lang_text = {
            'it': "operazione eliminata 🗑",
            'en': eng,
            'hi': "कार्रवाई हटा दी गई 🗑",
            'es': "operación eliminada 🗑",
            'fr': "opération supprimée 🗑",
            'de': "Operation gelöscht 🗑",
            'ru': "операция удалена 🗑",
            'uk': "операцію видалено 🗑",
            'zh': "操作已删除 🗑",
            'ar': "تم حذف العملية 🗑"
        }
        return lang_text.get(language_code, eng)
    
    def not_member_channel(self, language_code):
        channel_link = '<a href="https://t.me/tasu_Channel">👇</a>'
        eng = f"Join the channel to take advantage of the function! {channel_link}"
        lang_text = {
            'it': f"Entra nel canale per usufruire della funzione! {channel_link}",
            'en': eng,
            'hi': f"कार्रवाई का लाभ उठाने के लिए चैनल में शामिल हों! {channel_link}",
            'es': f"¡Entra al canal para utilizar esta función! {channel_link}",
            'fr': f"Inscrivez-vous sur le canal pour bénéficier de la fonctionnalité! {channel_link}",
            'de': f"Tritt dem Kanal bei, um die Funktion zu nutzen! {channel_link}",
            'ru': f"Вступите в канал, чтобы воспользоваться функцией! {channel_link}",
            'uk': f"Приєднуйтесь до каналу, щоб скористатися функцією! {channel_link}",
            'zh': f"加入频道以利用此功能！{channel_link}",
            'ar': f"انضم إلى القناة للاستفادة من الوظيفة! {channel_link}"
        }
        return lang_text.get(language_code, eng)
    
    def max_capacity(self, language_code):
        eng = 'Sorry, for now there is a maximum capacity for creating this QR code!'
        lang_text = {
            'it': 'Spiacente, al momento c\'è una capacità massima per creare questo codice QR!',
            'en': eng,
            'hi': 'क्षमा करें, अब इस QR कोड बनाने के लिए एक अधिकतम क्षमता है!',
            'es': 'Lo siento, por ahora hay una capacidad máxima para crear este código QR.',
            'fr': "Désolé, pour l'instant il y a une capacité maximale pour créer ce code QR !",
            'de': 'Entschuldigung, im Moment gibt es eine maximale Kapazität für die Erstellung dieses QR-Codes!',
            'ru': 'Извините, на данный момент есть максимальная емкость для создания этого QR-кода!',
            'uk': 'Вибачте, наразі існує максимальна місткість для створення цього QR-коду!',
            'zh': '抱歉，目前创建此QR代码的最大容量已达上限！',
            'ar': 'عذرًا، في الوقت الحالي هناك سعة قصوى لإنشاء هذا الرمز الشريطي!'
        }
        return lang_text.get(language_code, eng)

    def language_setting(self, language_code):
        eng = "Language setting 🇬🇧"
        lang_text = {
            'it': "Impostazioni Lingua 🇮🇹",
            'en': eng,
            'hi': "भाषा सेटिंग 🇮🇳",
            'es': "Configuración de Idioma 🇪🇸",
            'fr': "Paramètres de Langue 🇫🇷",
            'de': "Spracheinstellungen 🇩🇪",
            'ru': "Настройки Языка 🇷🇺",
            'uk': "Налаштування Мови 🇺🇦",
            'zh': "语言设置 🇨🇳",
            'ar': "إعداد اللغة 🇸🇦"
        }
        return lang_text.get(language_code, eng)
    
    def choose_language(self, language_code):
        lang_text = {
            'it': "Scegli la lingua 🇮🇹",
            'en': "Choose language 🇺🇸",
            'hi': "भाषा चुनें 🇮🇳",
            'es': "Elige el idioma 🇪🇸",
            'fr': "Choisissez la langue 🇫🇷",
            'de': "Wähle die Sprache 🇩🇪",
            'ru': "Выберите язык 🇷🇺",
            'uk': "Оберіть мову 🇺🇦",
            'zh': "选择语言 🇨🇳",
            'ar': "اختر اللغة 🇸🇦"
        }
        return lang_text.get(language_code, "Choose language 🌐")

    def language_setted(self, language_code):
        eng = f"Language setted 🇬🇧"
        if language_code == 'it':
            message = f"Lingua impostata 🇮🇹"
        elif language_code == 'en':
            message = eng
        elif language_code == 'hi':
            message = f"भाषा सेट की गई 🇮🇳"
        elif language_code == 'es':
            message = f"Idioma establecido 🇪🇸"
        elif language_code == 'fr':
            message = f"Langue définie 🇫🇷"
        elif language_code == 'de':
            message = f"Sprache festgelegt 🇩🇪"
        elif language_code == 'ru':
            message = f"Установлен язык 🇷🇺"
        elif language_code == 'uk':
            message = f"Мова встановлена 🇺🇦"
        elif language_code == 'zh':
            message = f"语言已设置 🇨🇳"
        elif language_code == 'ar':
            message = f"تم تعيين اللغة 🇸🇦"
        else:
            message = eng
        return message
    
    def wait_operation(self, language_code):
        eng = "Please wait for the operation to complete ⏳"
        lang_text = {
            'it': "Attendi il completamento dell'operazione ⏳",
            'en': eng,
            'hi': "कृपया कार्रवाई पूर्ण होने की प्रतीक्षा करें ⏳",
            'es': "Espere a que la operación se complete ⏳",
            'fr': "Veuillez patienter pendant que l'opération se termine ⏳",
            'de': "Bitte warten Sie, bis die Operation abgeschlossen ist ⏳",
            'ru': "Пожалуйста, подождите завершения операции ⏳",
            'uk': "Будь ласка, зачекайте завершення операції ⏳",
            'zh': "请等待操作完成 ⏳",
            'ar': "يرجى الانتظار حتى اكتمال العملية ⏳"
        }
        return lang_text.get(language_code, eng)
    
    def ai_qrcode(self, language_code):
        eng = "AI Qrcode 🤖"
        lang_text = {
            'it': "Codice QR AI 🤖",
            'en': eng,
            'hi': "एआई क्यूआरकोड 🤖",
            'es': "Código QR de IA 🤖",
            'fr': "QR code IA 🤖",
            'de': "KI-Qrcode 🤖",
            'ru': "QR-код ИИ 🤖",
            'uk': "QR-код ШІ 🤖",
            'zh': "AI 二维码 🤖",
            'ar': "رمز الاستجابة السريعة الذكاء الصناعي 🤖"
        }
        return lang_text.get(language_code, eng)

    def send_prompt(self, language_code):
        eng = "Send me a prompt 📬"
        lang_text = {
            'it': "Inviami un prompt 📬",
            'en': eng,
            'hi': "मुझे एक प्रोम्प्ट भेजें 📬",
            'es': "Envíame un mensaje 📬",
            'fr': "Envoyez-moi un message 📬",
            'de': "Schick mir einen Prompt 📬",
            'ru': "Отправьте мне подсказку 📬",
            'uk': "Надішли мені підказку 📬",
            'zh': "发送提示 📬",
            'ar': "أرسل لي تلميحًا 📬"
        }
        return lang_text.get(language_code)
    
    def save_action(self, language_code):
        eng = "Save 💾"
        lang_text = {
            'it': "Salva 💾",
            'en': eng,
            'hi': "सहेजें 💾",
            'es': "Guardar 💾",
            'fr': "Enregistrer 💾",
            'de': "Speichern 💾",
            'ru': "Сохранить 💾",
            'uk': "Зберегти 💾",
            'zh': "保存 💾",
            'ar': "احفظ 💾"
        }
        return lang_text.get(language_code, eng)
    
    def special_format_example(self, language_code):
        eng = "Copy for example:\n`MECARD:N:YOUR_NAME,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
        eng += "`WIFI:T:WPA;S:My network;P:secret;;`"
        lang_text = {
            'it': "Copia ad esempio:\n`MECARD:N:TUO_NOME,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:Mia rete;P:segreto;;`",
            'hi': "उदाहरण के लिए कॉपी करें:\n`MECARD:N:आपका_नाम,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:मेरा नेटवर्क;P:रहस्य;;`",
            'es': "Copia por ejemplo:\n`MECARD:N:SU_NOMBRE,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:Mi red;P:secreto;;`",
            'fr': "Copiez par exemple:\n`MECARD:N:VOTRE_NOM,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:Mon réseau;P:secret;;`",
            'de': "Kopieren Sie zum Beispiel:\n`MECARD:N:DEIN_NAME,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:Mein Netzwerk;P:geheim;;`",
            'ru': "Скопируйте, например:\n`MECARD:N:ВАШЕ_ИМЯ,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:Моя сеть;P:секрет;;`",
            'uk': "Скопіюйте, наприклад:\n`MECARD:N:ВАШЕ_ІМ'Я,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:Моя мережа;P:секрет;;`",
            'zh': "例如复制:\n`MECARD:N:你的名字,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:我的网络;P:秘密;;`",
            'ar': "انسخ على سبيل المثال:\n`MECARD:N:اسمك,Tasuboyz;URL:https://t.me/tasu_Channel;URL:https://web.telegram.org;EMAIL:example@gmail.com;TEL:+12345;`\n"
                "`WIFI:T:WPA;S:شبكتي;P:سري;;`"
        }
        return lang_text.get(language_code, eng)

    def text_saved(self, language_code):
        eng = "Text saved ✅"
        lang_text = {
            'it': "Testo salvato ✅",
            'en': eng,
            'hi': "पाठ सहेजा गया ✅",
            'es': "Texto guardado ✅",
            'fr': "Texte sauvegardé ✅",
            'de': "Text gespeichert ✅",
            'ru': "Текст сохранен ✅",
            'uk': "Текст збережено ✅",
            'zh': "文字已保存 ✅",
            'ar': "تم حفظ النص ✅"
        }
        return lang_text.get(language_code, eng)
    
    def gif_size_exceeded(self, language_code, max_size):
        eng = f"Sorry... The size of the gif file is more than {max_size}MB.🚫 \nIf you want to increase the capacity, upgrade to the premium plan 💎"
        lang_text = {
            'it': f"Spiacente... Le dimensioni del file gif sono superiori a {max_size}MB.🚫 \nSe vuoi aumentare la capacità, passa al piano premium 💎",
            'en': eng,
            'hi': f"क्षमा करें... GIF फ़ाइल का आकार {max_size}MB से अधिक है।🚫 \nअगर आप क्षमता बढ़ाना चाहते हैं, तो प्रीमियम प्लान पर अपग्रेड करें 💎",
            'es': f"Lo siento... El tamaño del archivo gif es mayor que {max_size}MB.🚫 \nSi deseas aumentar la capacidad, actualiza al plan premium 💎",
            'fr': f"Désolé... La taille du fichier gif est supérieure à {max_size}MB.🚫 \nSi vous souhaitez augmenter la capacité, passez au plan premium 💎",
            'de': f"Entschuldigung... Die Größe der GIF-Datei ist größer als {max_size}MB.🚫 \nWenn Sie die Kapazität erhöhen möchten, wechseln Sie zum Premium-Tarif 💎",
            'ru': f"Извините... Размер файла gif превышает {max_size}MB.🚫 \nЕсли вы хотите увеличить емкость, обновитесь до премиум-плана 💎",
            'uk': f"Вибачте... Розмір файлу gif перевищує {max_size}MB.🚫 \nЯкщо ви хочете збільшити ємність, оновіться до преміум-плану 💎",
            'zh': f"抱歉... GIF 文件的大小超过了 {max_size}MB.🚫 \n如果您想增加容量，请升级到高级套餐 💎",
            'ar': f"آسف... حجم ملف GIF أكبر من {max_size}MB.🚫 \nإذا كنت ترغب في زيادة السعة، فانتقل إلى الخطة المميزة 💎"
        }
        return lang_text.get(language_code, eng)
    
    def buy_premium_pack(self, language_code):
        eng = "Buy the Premium Pack 🛒💎"
        lang_text = {
            'it': "Acquista il Pacchetto Premium 🛒💎",
            'en': eng,
            'hi': "प्रीमियम पैक खरीदें 🛒💎",
            'es': "Compra el Paquete Premium 🛒💎",
            'fr': "Acheter le Pack Premium 🛒💎",
            'de': "Kaufen Sie das Premium-Paket 🛒💎",
            'ru': "Купить премиум-пакет 🛒💎",
            'uk': "Купити преміум-пакет 🛒💎",
            'zh': "购买高级套餐 🛒💎",
            'ar': "شراء حزمة البريميوم 🛒💎"
        }
        return lang_text.get(language_code, eng)
    
    def select_to_customize(self, language_code):
        eng = "Select to customize: 🎨"
        lang_text = {
            'it': "Seleziona per personalizzare: 🎨",
            'hi': "कस्टमाइज़ करने के लिए चुनें: 🎨",
            'es': "Selecciona para personalizar: 🎨",
            'fr': "Sélectionnez pour personnaliser: 🎨",
            'de': "Wählen Sie zur Anpassung aus: 🎨",
            'ru': "Выберите для настройки: 🎨",
            'uk': "Виберіть для налаштування: 🎨",
            'zh': "选择以自定义：🎨",
            'ar': "اختر للتخصيص: 🎨"
        }
        return lang_text.get(language_code, eng)

    def custom_version(self, language_code):
        eng = "version"
        return

    def get_result_language_strings(self, language_code):
        # Ottieni le stringhe di lingua corrispondenti al codice lingua
        waiting = self.waiting(language_code)
        error = self.error(language_code)
        code_not_found = self.code_not_found(language_code)
        return waiting, error, code_not_found
    
    def get_custom_language_strings(self, language_code, qr):
        # Ottieni le stringhe di lingua corrispondenti al codice lingua
        confirm = self.confirm(language_code, qr)
        previous_color = self.previous_color(language_code)
        back_text = self.back(language_code)
        ai_remover_on_text = '🤖 AI Remover 🚫'
        ai_remover_off_text = '🤖 AI Remover ✅'
        return confirm, back_text, previous_color, ai_remover_on_text, ai_remover_off_text

    def error_occurred(self, language_code):
        eng_message = "Oops... an error occurred, please try again or contact @tasuboyz immediately to show them the problem."
        lang_text = {
            'it': "ops... si è verificato un errore, riprova o contatta subito @tasuboyz per mostrargli il problema.",
            'hi': "उफ़... एक त्रुटि हुई है, कृपया पुनः प्रयास करें या समस्या दिखाने के लिए तुरंत @tasuboyz से संपर्क करें।",
            'es': "ups... ocurrió un error, intenta nuevamente o contacta a @tasuboyz inmediatamente para mostrarle el problema.",
            'fr': "oups... une erreur s'est produite, veuillez réessayer ou contacter immédiatement @tasuboyz pour lui montrer le problème.",
            'de': "ups... ein Fehler ist aufgetreten, bitte versuche es erneut oder kontaktiere sofort @tasuboyz, um ihnen das Problem zu zeigen.",
            'ru': "упс... произошла ошибка, пожалуйста, попробуйте снова или немедленно свяжитесь с @tasuboyz, чтобы показать им проблему.",
            'uk': "упс... сталася помилка, будь ласка, спробуйте ще раз або негайно зв'яжіться з @tasuboyz, щоб показати їм проблему.",
            'zh': "哎呀... 出现错误，请重试或立即联系 @tasuboyz 以向他们展示问题。",
            'ar': "عذرًا... حدث خطأ، يرجى المحاولة مرة أخرى أو الاتصال بـ @tasuboyz فورًا لإظهار المشكلة."
        }
        return lang_text.get(language_code, eng_message)

    def customize_qr(self, language_code):
        eng = "Customize QR 🎨"
        lang_text = {
            'it': "Personalizza QR 🎨",
            'en': eng,
            'hi': "क्यूआर को अनुकूलित करें 🎨",
            'es': "Personalizar QR 🎨",
            'fr': "Personnaliser QR 🎨",
            'de': "QR anpassen 🎨",
            'ru': "Настроить QR 🎨",
            'uk': "Налаштувати QR 🎨",
            'zh': "自定义 QR 🎨",
            'ar': "تخصيص QR 🎨"
        }
        return lang_text.get(language_code, eng)



