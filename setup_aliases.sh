#!/data/data/com.termux/files/usr/bin/bash
# ====================================================
# Byan - Setup Aliases
# لغة بيان للبرمجة باللغة العربية
# Author: Hossam Hassan Mohamed Hassan Ebid
# ====================================================

BYAN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BYAN_CLI="$BYAN_DIR/cli.py"

echo "🚀 إعداد aliases لبيان..."
echo ""

# ====================================================
# 1. إنشاء ملف الدالة
# ====================================================
cat > ~/.byan_aliases.sh << 'BYAN_FUNC_END'
#!/data/data/com.termux/files/usr/bin/bash

# دالة byan الذكية
function byan {
    local CLI="BYAN_CLI_PATH"
    
    if [ -z "$1" ]; then
        python "$CLI"
        return
    fi
    
    case "$1" in
        help|--help|-h|مساعدة)
            python "$CLI"
            return
            ;;
        نفّذ|run|exec|شغّل)
            if [ -z "$2" ]; then
                echo "❌ محتاج ملف"
                echo "   byan نفّذ ملف.byan"
                return 1
            fi
            python "$CLI" نفّذ "$2"
            return
            ;;
        ابنِ|build|compile)
            if [ -z "$2" ]; then
                echo "❌ محتاج ملف"
                echo "   byan ابنِ ملف.byan"
                return 1
            fi
            python "$CLI" ابنِ "$2"
            return
            ;;
        اختبر|test)
            python "$CLI" اختبر "${2:-tests/}"
            return
            ;;
        مكتبة|stdlib)
            python "$CLI" مكتبة
            return
            ;;
        تفاعل|repl)
            python "$CLI" تفاعل
            return
            ;;
    esac
    
    if [ -f "$1" ]; then
        python "$CLI" نفّذ "$1"
    else
        echo "❌ الملف مش موجود: $1"
        echo ""
        echo "الاستخدام:"
        echo "  byan ملف.byan          # تشغيل الملف"
        echo "  byan نفّذ ملف.byan     # تشغيل صريح"
        echo "  byan ابنِ ملف.byan     # تجميع"
        echo "  byan اختبر مجلد/       # اختبارات"
        echo "  byan مكتبة             # المكتبة"
        echo "  byan تفاعل             # REPL"
        echo "  byan --help            # المساعدة"
        return 1
    fi
}
BYAN_FUNC_END

# استبدل المسار بالمسار الفعلي
sed -i "s|BYAN_CLI_PATH|$BYAN_CLI|" ~/.byan_aliases.sh

# ====================================================
# 2. إضافة للـ bashrc
# ====================================================
if ! grep -q "byan_aliases.sh" ~/.bashrc 2>/dev/null; then
    echo "" >> ~/.bashrc
    echo "# Byan Aliases" >> ~/.bashrc
    echo '[ -f ~/.byan_aliases.sh ] && source ~/.byan_aliases.sh' >> ~/.bashrc
    echo "✅ تم إضافة الملف لـ ~/.bashrc"
else
    echo "ℹ️ الملف مضاف لـ ~/.bashrc مسبقًا"
fi

# ====================================================
# 3. إعادة تحميل
# ====================================================
source ~/.byan_aliases.sh

echo ""
echo "✅ تم الإعداد!"
echo ""
echo "🎁 جرب:"
echo "  byan --help"
echo "  byan ملف.byan"
echo "  byan مكتبة"
echo ""
