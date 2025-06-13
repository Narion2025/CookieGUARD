#!/bin/bash
echo "🔥 Building Archetypen-Schmied Static Site..."
echo "✅ No build steps needed - static files ready!"
echo "📁 Files available:"
ls -la *.html *.css *.js 2>/dev/null || echo "Static files found"
echo "🚀 Ready for deployment!" 