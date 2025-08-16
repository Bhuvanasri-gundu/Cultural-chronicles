"""
Sample data generator for Cultural Chronicles
Run this script to populate the database with sample cultural stories
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_sample_data():
    """Create sample cultural stories for testing"""
    try:
        from utils.data_manager import DataManager
        
        dm = DataManager()
        
        sample_stories = [
            {
                'title': 'The Legend of Birsa Munda',
                'original_text': '''बिरसा मुंडा एक महान स्वतंत्रता सेनानी और आदिवासी नेता थे। उन्होंने अंग्रेजी शासन के खिलाफ लड़ाई लड़ी और अपने लोगों के अधिकारों के लिए संघर्ष किया। वह 'धरती आबा' (पृथ्वी के पिता) के नाम से प्रसिद्ध थे। उनकी वीरता और त्याग की कहानियां आज भी झारखंड में गाई जाती हैं।''',
                'translated_text': '''Birsa Munda was a great freedom fighter and tribal leader. He fought against British rule and struggled for the rights of his people. He was famous as 'Dharti Aba' (Father of Earth). Stories of his bravery and sacrifice are still sung in Jharkhand today.''',
                'detected_language': 'Hindi',
                'category': 'Historical Account',
                'region': 'Jharkhand',
                'community': 'Munda',
                'story_type': 'Legend',
                'language_hint': 'Hindi',
                'image_path': None,
                'timestamp': (datetime.now() - timedelta(days=5)).isoformat()
            },
            {
                'title': 'Onam Festival Story',
                'original_text': '''ഓണം കേരളത്തിലെ ഏറ്റവും പ്രധാനപ്പെട്ട ഉത്സവമാണ്. രാജാവായ മഹാബലിയുടെ വാർഷിക വരവിനെ ആഘോഷിക്കുന്ന ഈ ഉത്സവം പത്ത് ദിവസം നീണ്ടുനിൽക്കുന്നു. വാമന അവതാരത്തിന്റെയും മഹാബലിയുടെയും കഥ ഈ ഉത്സവത്തിന്റെ പിന്നിലുണ്ട്. പൂക്കളം, സദ്യ, പുലികളി എന്നിവ ഓണത്തിന്റെ പ്രത്യേകതകളാണ്।''',
                'translated_text': '''Onam is the most important festival of Kerala. This festival celebrating the annual visit of King Mahabali lasts for ten days. The story of Vamana avatar and Mahabali is behind this festival. Pookalam (flower carpet), Sadhya (feast), and Pulikali (tiger dance) are the specialties of Onam.''',
                'detected_language': 'Malayalam',
                'category': 'Festival',
                'region': 'Kerala',
                'community': 'Malayalam',
                'story_type': 'Festival',
                'language_hint': 'Malayalam',
                'image_path': None,
                'timestamp': (datetime.now() - timedelta(days=3)).isoformat()
            },
            {
                'title': 'The Story of Sohrai Festival',
                'original_text': '''Sohrai is an ancient harvest festival celebrated by tribal communities in Jharkhand, West Bengal, and Odisha. During this festival, cattle are worshipped as they are considered sacred and important for agriculture. Women create beautiful wall paintings using natural colors made from clay, charcoal, and flowers. The festival symbolizes the bond between humans, animals, and nature.''',
                'translated_text': None,
                'detected_language': 'English',
                'category': 'Festival',
                'region': 'Jharkhand',
                'community': 'Tribal',
                'story_type': 'Tradition',
                'language_hint': 'English',
                'image_path': None,
                'timestamp': (datetime.now() - timedelta(days=7)).isoformat()
            },
            {
                'title': 'తెలుగు వంటకం - పెసర అట్టు',
                'original_text': '''పెసరకు గిన్నె అట్టు తెలుగు వారి ప్రముఖ వంటకం. ముఖ్యంగా గణేశ చవిति రోజున చేస్తారు. పెసరపప్పు, బియ్యం కలిపి నానబెట్టి రాతిరోజుల వేసుకొని అట్లు చేస్తారు. వీటితో పచ్చి చట్నీ, కొబ్బరి చట్నీ తింటారు. ఈ అట్లు చాలా రుచిగా మరియు ఆరోగ్యంగా ఉంటాయి.''',
                'translated_text': '''Pesara Attu (Moong Dal Pancakes) is a famous Telugu dish. It is especially made on Ganesh Chaturthi day. Moong dal and rice are soaked together and ground on stone to make these pancakes. They are eaten with green chutney and coconut chutney. These pancakes are very tasty and healthy.''',
                'detected_language': 'Telugu',
                'category': 'Recipe',
                'region': 'Telangana',
                'community': 'Telugu',
                'story_type': 'Recipe',
                'language_hint': 'Telugu',
                'image_path': None,
                'timestamp': (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                'title': 'The Peacock and the Crow - Tamil Folk Tale',
                'original_text': '''ஒரு மயில் மற்றும் ஒரு காகம் நண்பர்களாக இருந்தனர். மயில் தன் அழகான இறகுகளைப் பற்றி பெருமிதம் கொண்டிருந்தது. ஒரு நாள் பெரிய புயல் வந்தது. மயிலால் பறக்க முடியவில்லை, ஆனால் காகம் எளிதாக பறந்து சென்றது. இதிலிருந்து மயில் புரிந்துகொண்டது - அழகை விட திறமை முக்கியம்.''',
                'translated_text': '''A peacock and a crow were friends. The peacock was proud of its beautiful feathers. One day a big storm came. The peacock could not fly, but the crow flew easily. From this the peacock understood - skill is more important than beauty.''',
                'detected_language': 'Tamil',
                'category': 'Folk Tale',
                'region': 'Tamil Nadu',
                'community': 'Tamil',
                'story_type': 'Folk Tale',
                'language_hint': 'Tamil',
                'image_path': None,
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                'title': 'Durga Puja Tradition in Bengal',
                'original_text': '''দুর্গাপূজা বাঙালিদের সবচেয়ে বড় উৎসব। এই সময় দেবী দুর্গা তার সন্তানদের নিয়ে মর্ত্যে আসেন। প্রতিটি পাড়ায় প্যান্ডেল তৈরি হয়। মানুষ নতুন কাপড় পরে, মিষ্টি খায়, আর পূজা দেখতে যায়। ঢাকের তালে তালে সবাই নাচে। এই পাঁচদিন বাঙালিরা সব দুঃখ ভুলে আনন্দে মেতে থাকে।''',
                'translated_text': '''Durga Puja is the biggest festival of Bengalis. During this time, Goddess Durga comes to earth with her children. Pandals are set up in every neighborhood. People wear new clothes, eat sweets, and go to see the puja. Everyone dances to the rhythm of drums. During these five days, Bengalis forget all sorrows and immerse themselves in joy.''',
                'detected_language': 'Bengali',
                'category': 'Festival',
                'region': 'West Bengal',
                'community': 'Bengali',
                'story_type': 'Tradition',
                'language_hint': 'Bengali',
                'image_path': None,
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        success_count = 0
        for story in sample_stories:
            if dm.save_story(story):
                success_count += 1
                print(f"✅ Saved: {story['title']}")
            else:
                print(f"❌ Failed to save: {story['title']}")
        
        print(f"\n🎉 Successfully created {success_count} out of {len(sample_stories)} sample stories!")
        
        # Show statistics
        stats = dm.get_statistics()
        print(f"\n📊 Archive Statistics:")
        print(f"- Total Stories: {stats['total_stories']}")
        print(f"- Languages: {stats['unique_languages']}")
        print(f"- Recent Languages: {', '.join(stats['recent_languages'][:3])}")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")

if __name__ == "__main__":
    print("🚀 Creating sample data for Cultural Chronicles...")
    create_sample_data()
