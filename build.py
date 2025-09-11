import os
import shutil
from jinja2 import Environment, FileSystemLoader
import markdown
import yaml

# --- КОНФИГУРАЦИЯ ПРОЕКТА ---
# Определяем пути к папкам, чтобы легко их менять в одном месте
CONTENT_PATH = 'content'
TEMPLATE_PATH = 'templates'
STATIC_PATH = 'static'
OUTPUT_PATH = 'output'

# --- ШАГ 1: ОЧИСТКА ПРЕДЫДУЩЕЙ ВЕРСИИ ---
# Перед каждой сборкой полностью удаляем старую папку output, чтобы избежать мусора
print("🧹 Очистка старой версии сайта...")
if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.makedirs(OUTPUT_PATH) # Создаем пустую папку output

# --- ШАГ 2: КОПИРОВАНИЕ СТАТИЧЕСКИХ ФАЙЛОВ ---
# Просто копируем все стили, картинки и шрифты в папку output
print("🎨 Копирование стилей и картинок...")
# Путь к папке static теперь относительный, что более корректно
shutil.copytree(STATIC_PATH, os.path.join(OUTPUT_PATH, 'static'))

# --- ШАГ 3: НАСТРОЙКА ШАБЛОНИЗАТОРА JINJA2 ---
# Создаем окружение Jinja2 и указываем ему, где лежат наши HTML-шаблоны
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

# --- ШАГ 4: ЗАГРУЗКА ВСЕХ ДАННЫХ ---
print("📚 Загрузка структуры и контента техник...")

# Загружаем главный файл структуры из YAML
with open(os.path.join(CONTENT_PATH, 'structure.yml'), 'r', encoding='utf-8') as f:
    structure_data = yaml.safe_load(f)

# Загружаем все техники из папки content/techniques
techniques_data = {} # Создаем пустой словарь для хранения данных техник
techniques_path = os.path.join(CONTENT_PATH, 'techniques')
for filename in os.listdir(techniques_path):
    if filename.endswith('.md'):
        # Получаем id техники из имени файла (например, 'svidetel-ne-sudya')
        technique_id = filename.replace('.md', '')
        filepath = os.path.join(techniques_path, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            # Читаем весь файл и разделяем его на метаданные (между '---') и основной контент
            content_raw = f.read()
            parts = content_raw.split('---', 2)
            metadata_raw = parts[1]
            content_md = parts[2]
            
            # Превращаем метаданные из текста в словарь
            metadata = yaml.safe_load(metadata_raw)
            # Превращаем основной контент из Markdown в HTML
            content_html = markdown.markdown(content_md)
            
            # Сохраняем все данные о технике в наш словарь
            techniques_data[technique_id] = {
                'id': technique_id,
                'title': metadata.get('title', 'Без названия'),
                'subtitle': metadata.get('subtitle', ''),
                'icon': metadata.get('icon', ''),
                'content': content_html
            }

# --- ШАГ 5: ГЕНЕРАЦИЯ HTML-СТРАНИЦ ---
print("🚀 Генерация HTML-страниц...")

# 5.1. Главная страница (index.html)
template = env.get_template('index.html') # Берем шаблон
# Вставляем в шаблон данные о "болях"
output_content = template.render(pains=structure_data['pains']) 
# Записываем готовую HTML-страницу в файл
with open(os.path.join(OUTPUT_PATH, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(output_content)
print("  - Главная страница создана.")

# 5.2. Страницы категорий "болей"
template = env.get_template('pain_category.html') # Берем нужный шаблон
for pain in structure_data['pains']:
    pain_id = pain['id']
    
    # Для каждой категории собираем полный список данных о ее техниках
    category_techniques = []
    for tech_id in pain['techniques']:
        if tech_id in techniques_data:
            category_techniques.append(techniques_data[tech_id])

    # Вставляем данные в шаблон
    output_content = template.render(pain=pain, techniques=category_techniques)
    
    # Создаем папку для категории (например, 'output/verdikt/') и записываем туда файл index.html
    os.makedirs(os.path.join(OUTPUT_PATH, pain_id), exist_ok=True)
    with open(os.path.join(OUTPUT_PATH, pain_id, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output_content)
    print(f"  - Страница категории '{pain_id}' создана.")

# 5.3. Страницы самих техник
template = env.get_template('technique.html') # Берем шаблон для карточки техники
for tech_id, technique in techniques_data.items():
    output_content = template.render(technique=technique)
    
    # Создаем папку для техники (например, 'output/techniques/svidetel-ne-sudya/') и записываем файл
    os.makedirs(os.path.join(OUTPUT_PATH, 'techniques', tech_id), exist_ok=True)
    with open(os.path.join(OUTPUT_PATH, 'techniques', tech_id, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output_content)
    print(f"  - Страница техники '{tech_id}' создана.")

print("\n✅ Сборка успешно завершена! Готовый сайт находится в папке 'output'.")