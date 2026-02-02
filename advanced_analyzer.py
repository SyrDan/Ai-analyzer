"""
Продвинутый ML анализатор учебных текстов
Содержит дополнительные функции для глубокого анализа
"""

import re
from collections import Counter, defaultdict
import math


class AdvancedTextAnalyzer:
    """
    Расширенный анализатор с дополнительными ML функциями
    """
    
    def __init__(self):
        # Словари для классификации
        self.subject_keywords = {
            'программирование': ['код', 'функция', 'переменная', 'класс', 'объект', 'алгоритм', 'программа'],
            'математика': ['уравнение', 'формула', 'теорема', 'доказательство', 'функция', 'производная'],
            'физика': ['энергия', 'сила', 'скорость', 'движение', 'температура', 'волна'],
            'химия': ['реакция', 'элемент', 'молекула', 'атом', 'соединение', 'вещество'],
            'биология': ['клетка', 'организм', 'эволюция', 'ген', 'белок', 'ткань'],
            'история': ['война', 'революция', 'империя', 'государство', 'культура', 'событие'],
            'языки': ['грамматика', 'слово', 'предложение', 'глагол', 'существительное', 'текст']
        }
        
        self.learning_styles = {
            'визуальный': ['диаграмма', 'схема', 'график', 'таблица', 'рисунок', 'изображение'],
            'аудиальный': ['объяснение', 'лекция', 'дискуссия', 'обсуждение', 'диалог'],
            'практический': ['упражнение', 'практика', 'задача', 'проект', 'эксперимент', 'применение']
        }
    
    def detect_subject(self, text):
        """
        Определяет предметную область текста
        """
        text_lower = text.lower()
        scores = defaultdict(int)
        
        for subject, keywords in self.subject_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[subject] += text_lower.count(keyword)
        
        if not scores:
            return 'общий'
        
        return max(scores, key=scores.get)
    
    def suggest_learning_style(self, text):
        """
        Предлагает оптимальный стиль обучения на основе текста
        """
        text_lower = text.lower()
        scores = defaultdict(int)
        
        for style, keywords in self.learning_styles.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[style] += 1
        
        # Добавляем общий анализ структуры
        if text.count('```') > 0 or text.count('def ') > 0:
            scores['практический'] += 5
        
        if len(re.findall(r'\n\s*[-*]\s', text)) > 3:
            scores['визуальный'] += 3
        
        suggested_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if not suggested_styles:
            return ['практический', 'визуальный', 'аудиальный']
        
        return [style for style, score in suggested_styles[:2]]
    
    def calculate_readability(self, text):
        """
        Вычисляет индекс читабельности текста
        Упрощённая версия индекса Флеша
        """
        sentences = [s for s in text.split('.') if s.strip()]
        words = text.split()
        
        if not sentences or not words:
            return 50  # средний уровень
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Упрощённая формула (чем выше, тем легче читать)
        readability = 206.835 - 1.015 * avg_sentence_length - 84.6 * (avg_word_length / 5)
        
        # Нормализуем к шкале 0-100
        readability = max(0, min(100, readability))
        
        return round(readability, 1)
    
    def extract_questions(self, text):
        """
        Извлекает вопросы из текста для самопроверки
        """
        questions = re.findall(r'[А-ЯA-Z][^.!?]*\?', text)
        return questions[:5]  # возвращаем максимум 5 вопросов
    
    def generate_flashcards(self, text, keywords):
        """
        Генерирует карточки для запоминания на основе ключевых слов
        """
        flashcards = []
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        for keyword in keywords[:5]:
            # Находим предложение с этим ключевым словом
            for sentence in sentences:
                if keyword.lower() in sentence.lower():
                    flashcards.append({
                        'front': f"Что такое {keyword}?",
                        'back': sentence,
                        'keyword': keyword
                    })
                    break
        
        return flashcards
    
    def identify_prerequisites(self, text, subject):
        """
        Определяет предварительные знания, необходимые для изучения
        """
        prerequisites_map = {
            'программирование': ['Базовая компьютерная грамотность', 'Логическое мышление', 'Английский язык (базовый)'],
            'математика': ['Арифметика', 'Базовая алгебра', 'Логическое мышление'],
            'физика': ['Математика (алгебра)', 'Базовые понятия о природе'],
            'химия': ['Математика', 'Базовые понятия о веществах'],
            'биология': ['Общие знания о живых организмах'],
            'история': ['Хронологическое мышление', 'География (базовая)'],
            'языки': ['Родной язык (хорошее знание)', 'Базовая грамматика']
        }
        
        # Базовые предварительные требования
        base_prerequisites = prerequisites_map.get(subject, ['Базовая грамотность', 'Желание учиться'])
        
        # Анализируем сложность текста для дополнительных требований
        text_lower = text.lower()
        
        advanced_keywords = ['продвинутый', 'сложный', 'advanced', 'комплексный', 'интегрированный']
        if any(keyword in text_lower for keyword in advanced_keywords):
            base_prerequisites.insert(0, f'Средний уровень знаний в {subject}')
        
        return base_prerequisites
    
    def calculate_engagement_score(self, text):
        """
        Оценивает насколько текст вовлекающий и интересный
        """
        score = 50  # базовый балл
        
        text_lower = text.lower()
        
        # Положительные факторы
        engaging_words = ['интересно', 'важно', 'удивительно', 'представьте', 'давайте', 'почему', 'как']
        score += sum(2 for word in engaging_words if word in text_lower)
        
        # Наличие примеров
        if 'например' in text_lower or 'пример' in text_lower:
            score += 10
        
        # Наличие вопросов
        score += text.count('?') * 3
        
        # Наличие списков
        score += len(re.findall(r'\n\s*[-*•]\s', text)) * 2
        
        # Слишком длинные предложения уменьшают вовлечённость
        sentences = text.split('.')
        if sentences:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_length > 25:
                score -= 10
        
        return max(0, min(100, score))
    
    def generate_study_notes_template(self, text, keywords):
        """
        Генерирует шаблон конспекта для студента
        """
        template = {
            'title': 'Конспект по материалу',
            'date': 'Дата изучения: __________',
            'key_points': [
                '1. ___________________________________',
                '2. ___________________________________',
                '3. ___________________________________',
                '4. ___________________________________',
                '5. ___________________________________'
            ],
            'keywords_to_remember': keywords[:8],
            'questions_to_answer': [
                'Q: Какова основная идея?',
                'A: ___________________________________',
                '',
                'Q: Как это применяется на практике?',
                'A: ___________________________________',
                '',
                'Q: С чем это связано?',
                'A: ___________________________________'
            ],
            'summary_space': 'Краткое резюме своими словами:\n' + '_' * 50 + '\n' * 5,
            'reflection': 'Что я узнал нового?\n' + '_' * 50 + '\n' * 3
        }
        
        return template
    
    def analyze_comprehensive(self, text):
        """
        Комплексный анализ текста со всеми метриками
        """
        from collections import Counter
        
        # Базовая статистика
        words = re.findall(r'\b[а-яa-z]+\b', text.lower())
        sentences = [s for s in text.split('.') if s.strip()]
        
        # Ключевые слова
        stop_words = {'это', 'как', 'что', 'для', 'или', 'который', 'the', 'is', 'and', 'or'}
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
        keywords = [word for word, count in Counter(filtered_words).most_common(10)]
        
        # Определяем предмет
        subject = self.detect_subject(text)
        
        # Стили обучения
        learning_styles = self.suggest_learning_style(text)
        
        # Читабельность
        readability = self.calculate_readability(text)
        
        # Вовлечённость
        engagement = self.calculate_engagement_score(text)
        
        # Генерируем карточки
        flashcards = self.generate_flashcards(text, keywords)
        
        # Предварительные требования
        prerequisites = self.identify_prerequisites(text, subject)
        
        # Шаблон конспекта
        notes_template = self.generate_study_notes_template(text, keywords)
        
        return {
            'basic_stats': {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'unique_words': len(set(words)),
                'avg_sentence_length': len(words) / max(len(sentences), 1)
            },
            'subject': subject,
            'keywords': keywords,
            'learning_styles': learning_styles,
            'readability_score': readability,
            'engagement_score': engagement,
            'prerequisites': prerequisites,
            'flashcards': flashcards,
            'notes_template': notes_template,
            'difficulty_interpretation': self._interpret_readability(readability)
        }
    
    def _interpret_readability(self, score):
        """
        Интерпретирует балл читабельности
        """
        if score >= 70:
            return {
                'level': 'Лёгкий',
                'description': 'Текст легко читается и понимается',
                'recommendation': 'Подходит для самостоятельного изучения'
            }
        elif score >= 50:
            return {
                'level': 'Средний',
                'description': 'Требует внимания и концентрации',
                'recommendation': 'Делайте заметки по ходу чтения'
            }
        else:
            return {
                'level': 'Сложный',
                'description': 'Сложный текст, требует глубокого изучения',
                'recommendation': 'Читайте по частям, используйте дополнительные источники'
            }


# Пример использования
if __name__ == '__main__':
    analyzer = AdvancedTextAnalyzer()
    
    sample_text = """
    Python - это высокоуровневый язык программирования общего назначения. 
    Он поддерживает множественные парадигмы программирования, включая процедурное, 
    объектно-ориентированное и функциональное программирование. Python широко используется 
    для веб-разработки, анализа данных, машинного обучения и автоматизации задач.
    """
    
    result = analyzer.analyze_comprehensive(sample_text)
    
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ ===")
    print(f"Предмет: {result['subject']}")
    print(f"Ключевые слова: {', '.join(result['keywords'][:5])}")
    print(f"Читабельность: {result['readability_score']} - {result['difficulty_interpretation']['level']}")
    print(f"Вовлечённость: {result['engagement_score']}/100")
    print(f"Рекомендуемые стили обучения: {', '.join(result['learning_styles'])}")
