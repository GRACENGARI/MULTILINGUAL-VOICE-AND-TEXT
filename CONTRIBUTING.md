# Contributing to African Language AI Tutor

Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## 🌍 How to Contribute

### 1. Language Content
- Add new vocabulary to JSON files in `language_data/`
- Expand grammar rules with examples
- Include cultural context and usage notes
- Correct any errors in existing content

### 2. Code Contributions
- Fix bugs
- Add new features
- Improve performance
- Enhance UI/UX

### 3. Documentation
- Improve README and guides
- Add tutorials and examples
- Translate documentation
- Create video tutorials

### 4. Testing
- Test with native speakers
- Report bugs and issues
- Suggest improvements
- Validate translations

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/MULTILINGUAL-VOICE-AND-TEXT.git
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test your changes**
   ```bash
   streamlit run african_language_tutor.py
   ```
6. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request**

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

- `Add: new feature or content`
- `Fix: bug fix`
- `Update: improvements to existing code`
- `Docs: documentation changes`
- `Style: formatting, no code change`
- `Refactor: code restructuring`
- `Test: adding tests`

## 🎯 Priority Areas

### High Priority
- [ ] Native speaker validation of language content
- [ ] Speech recognition implementation
- [ ] Pronunciation assessment
- [ ] Mobile app development

### Medium Priority
- [ ] Additional African languages
- [ ] Offline mode
- [ ] Gamification features
- [ ] Teacher dashboard

### Low Priority
- [ ] UI themes
- [ ] Additional quiz types
- [ ] Social features
- [ ] Analytics dashboard

## 🌟 Language Content Guidelines

When adding language content to JSON files:

### Vocabulary
```json
{
  "word": {
    "meaning": "English translation",
    "pos": "noun/verb/adjective/etc",
    "examples": [
      "Example sentence in target language",
      "Another example with context"
    ],
    "cultural_note": "Optional cultural context"
  }
}
```

### Grammar Rules
```json
{
  "rule": "Rule name",
  "description": "Clear explanation",
  "examples": [
    "Example 1",
    "Example 2"
  ]
}
```

### Common Errors
```json
{
  "error": "Common mistake",
  "correct": "Correct usage",
  "example": "Example showing correction"
}
```

## 🔍 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions
- Keep functions focused and small

## 🧪 Testing

Before submitting:

1. Test the application runs without errors
2. Verify new features work as expected
3. Check that existing features still work
4. Test with different languages
5. Validate voice features if applicable

## 📞 Questions?

- Open an issue for questions
- Join discussions in Issues tab
- Contact maintainers

## 🙏 Thank You!

Every contribution, no matter how small, helps preserve and promote African languages in the digital space. Thank you for being part of this mission!

---

**Together, we're building a better future for African language education! 🌍✨**