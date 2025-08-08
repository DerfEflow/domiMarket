"""
Trend Discovery Service
Searches for viral memes, trends, and cultural moments to incorporate into marketing content
"""

import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class TrendDiscoveryService:
    """Service to discover viral trends, memes, and cultural moments"""
    
    def __init__(self):
        self.trend_sources = self._get_trend_sources()
        self.cache_duration = 3600  # 1 hour cache
        self._trend_cache = {}
    
    def discover_viral_trends(self, industry: str = None, target_audience: str = None) -> List[Dict[str, Any]]:
        """Discover current viral trends and memes"""
        
        cache_key = f"trends_{industry}_{target_audience}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            logger.info("Returning cached trends")
            return self._trend_cache[cache_key]['data']
        
        try:
            trends = []
            
            # Get trends from multiple sources
            google_trends = self._get_google_trends(industry)
            social_trends = self._get_social_media_trends()
            meme_trends = self._get_meme_trends()
            cultural_moments = self._get_cultural_moments()
            
            # Combine and score trends
            all_trends = google_trends + social_trends + meme_trends + cultural_moments
            
            # Filter and rank trends
            filtered_trends = self._filter_and_rank_trends(
                all_trends, industry, target_audience
            )
            
            # Cache results
            self._trend_cache[cache_key] = {
                'timestamp': datetime.utcnow(),
                'data': filtered_trends[:10]  # Top 10 trends
            }
            
            logger.info(f"Discovered {len(filtered_trends)} viral trends")
            return filtered_trends[:10]
            
        except Exception as e:
            logger.error(f"Error discovering trends: {str(e)}")
            return self._get_fallback_trends()
    
    def _get_google_trends(self, industry: str = None) -> List[Dict[str, Any]]:
        """Get trending topics from Google Trends (simulated data structure)"""
        
        # In production, this would use Google Trends API or web scraping
        # For now, returning structured trending topics
        
        trending_topics = [
            {
                'type': 'search_trend',
                'title': 'AI productivity hacks',
                'description': 'People are obsessed with AI tools that actually save time',
                'engagement_score': 95,
                'relevance_score': 90 if industry and 'tech' in industry.lower() else 70,
                'platform': 'google',
                'viral_factor': 'Productivity anxiety meets AI hope',
                'usage_tip': 'Position your service as the AI solution that actually delivers'
            },
            {
                'type': 'search_trend', 
                'title': 'Quiet luxury trend',
                'description': 'Understated wealth and minimalist aesthetics',
                'engagement_score': 88,
                'relevance_score': 85 if industry and any(x in industry.lower() for x in ['fashion', 'luxury', 'design']) else 60,
                'platform': 'google',
                'viral_factor': 'Reaction against flashy consumption',
                'usage_tip': 'Emphasize quality, craftsmanship, and subtle sophistication'
            },
            {
                'type': 'search_trend',
                'title': 'Micro-dosing productivity',
                'description': 'Small, consistent improvements over big changes',
                'engagement_score': 82,
                'relevance_score': 75,
                'platform': 'google',
                'viral_factor': 'Overwhelm fatigue, people want sustainable progress',
                'usage_tip': 'Frame your solution as a small daily habit that compounds'
            }
        ]
        
        return trending_topics
    
    def _get_social_media_trends(self) -> List[Dict[str, Any]]:
        """Get viral content from social media platforms"""
        
        # In production, this would use social media APIs
        social_trends = [
            {
                'type': 'meme_format',
                'title': 'Corporate needs you to find the difference',
                'description': 'Pointing out how similar competing solutions actually are',
                'engagement_score': 92,
                'relevance_score': 80,
                'platform': 'twitter/tiktok',
                'viral_factor': 'Everyone is tired of the same generic solutions',
                'usage_tip': 'Use this to highlight what actually makes you different'
            },
            {
                'type': 'cultural_moment',
                'title': 'January gym influx',
                'description': 'New Year resolution gym crowding and eventual emptying',
                'engagement_score': 89,
                'relevance_score': 70,
                'platform': 'instagram/tiktok',
                'viral_factor': 'Universal experience of good intentions vs reality',
                'usage_tip': 'Frame your service as the sustainable alternative to failed resolutions'
            },
            {
                'type': 'viral_phrase',
                'title': 'Very demure, very mindful',
                'description': 'Describing modest, thoughtful behavior in a playful way',
                'engagement_score': 85,
                'relevance_score': 65,
                'platform': 'tiktok',
                'viral_factor': 'Ironic sophistication, plays with expectations',
                'usage_tip': 'Use for brands wanting to appear humble yet confident'
            }
        ]
        
        return social_trends
    
    def _get_meme_trends(self) -> List[Dict[str, Any]]:
        """Get current meme formats and viral content"""
        
        meme_trends = [
            {
                'type': 'meme_format',
                'title': 'This is fine dog in burning room',
                'description': 'Pretending everything is okay when it clearly isn\'t',
                'engagement_score': 90,
                'relevance_score': 85,
                'platform': 'reddit/twitter',
                'viral_factor': 'Universal feeling of maintaining composure during chaos',
                'usage_tip': 'Perfect for positioning your solution as the calm in the storm'
            },
            {
                'type': 'viral_sound',
                'title': 'Oh no, oh no, oh no no no no no',
                'description': 'Audio used for showing things going progressively wrong',
                'engagement_score': 87,
                'relevance_score': 75,
                'platform': 'tiktok/instagram',
                'viral_factor': 'Captures the feeling of escalating problems',
                'usage_tip': 'Use to show problems your service prevents'
            },
            {
                'type': 'meme_format',
                'title': 'Drake pointing and rejecting',
                'description': 'Rejecting old way, pointing approvingly at new way',
                'engagement_score': 88,
                'relevance_score': 90,
                'platform': 'all_platforms',
                'viral_factor': 'Simple before/after comparison format',
                'usage_tip': 'Perfect for showing your solution vs outdated alternatives'
            }
        ]
        
        return meme_trends
    
    def _get_cultural_moments(self) -> List[Dict[str, Any]]:
        """Get current cultural moments and zeitgeist topics"""
        
        cultural_moments = [
            {
                'type': 'cultural_moment',
                'title': 'AI job displacement anxiety',
                'description': 'People worried about AI taking their jobs',
                'engagement_score': 93,
                'relevance_score': 85,
                'platform': 'linkedin/twitter',
                'viral_factor': 'Existential workplace anxiety meets technological change',
                'usage_tip': 'Position your service as empowering people, not replacing them'
            },
            {
                'type': 'cultural_moment',
                'title': 'Subscription fatigue',
                'description': 'Everyone is tired of paying for multiple monthly subscriptions',
                'engagement_score': 91,
                'relevance_score': 80,
                'platform': 'twitter/reddit',
                'viral_factor': 'Death by a thousand small charges',
                'usage_tip': 'Emphasize value, one-time payments, or consolidation benefits'
            },
            {
                'type': 'cultural_moment',
                'title': 'Return to office resistance',
                'description': 'Pushback against mandatory office returns',
                'engagement_score': 86,
                'relevance_score': 75,
                'platform': 'linkedin/twitter',
                'viral_factor': 'Work-life balance becomes non-negotiable',
                'usage_tip': 'Highlight flexibility and remote-friendly features'
            }
        ]
        
        return cultural_moments
    
    def _filter_and_rank_trends(self, trends: List[Dict[str, Any]], 
                               industry: str = None, 
                               target_audience: str = None) -> List[Dict[str, Any]]:
        """Filter and rank trends by relevance and engagement"""
        
        # Calculate composite scores
        for trend in trends:
            composite_score = (
                trend['engagement_score'] * 0.4 + 
                trend['relevance_score'] * 0.6
            )
            trend['composite_score'] = composite_score
            
            # Boost score for industry relevance
            if industry and self._is_industry_relevant(trend, industry):
                trend['composite_score'] += 10
            
            # Boost score for audience relevance
            if target_audience and self._is_audience_relevant(trend, target_audience):
                trend['composite_score'] += 5
        
        # Sort by composite score
        return sorted(trends, key=lambda x: x['composite_score'], reverse=True)
    
    def _is_industry_relevant(self, trend: Dict[str, Any], industry: str) -> bool:
        """Check if trend is relevant to specific industry"""
        
        industry_lower = industry.lower()
        trend_text = (trend['title'] + ' ' + trend['description']).lower()
        
        industry_keywords = {
            'technology': ['ai', 'tech', 'software', 'digital', 'automation'],
            'healthcare': ['health', 'medical', 'wellness', 'therapy', 'care'],
            'finance': ['money', 'financial', 'investment', 'subscription', 'payment'],
            'education': ['learning', 'productivity', 'skill', 'improvement'],
            'marketing': ['brand', 'content', 'social', 'engagement', 'viral'],
            'retail': ['shopping', 'consumer', 'luxury', 'product', 'purchase']
        }
        
        for category, keywords in industry_keywords.items():
            if category in industry_lower:
                return any(keyword in trend_text for keyword in keywords)
        
        return False
    
    def _is_audience_relevant(self, trend: Dict[str, Any], target_audience: str) -> bool:
        """Check if trend resonates with target audience"""
        
        audience_lower = target_audience.lower()
        
        # Age-based relevance
        if any(term in audience_lower for term in ['gen z', 'young', 'teen', 'student']):
            return trend['platform'] in ['tiktok', 'instagram']
        
        if any(term in audience_lower for term in ['millennial', 'professional']):
            return trend['platform'] in ['twitter', 'linkedin', 'instagram']
        
        if any(term in audience_lower for term in ['gen x', 'boomer', 'senior']):
            return trend['platform'] in ['facebook', 'linkedin']
        
        return True
    
    def get_trend_integration_suggestions(self, selected_trends: List[Dict[str, Any]], 
                                        campaign_goal: str, 
                                        brand_voice: str) -> List[Dict[str, Any]]:
        """Get specific suggestions for integrating trends into marketing content"""
        
        suggestions = []
        
        for trend in selected_trends:
            suggestion = {
                'trend': trend,
                'integration_approach': self._get_integration_approach(trend, campaign_goal, brand_voice),
                'content_ideas': self._generate_content_ideas(trend, campaign_goal, brand_voice),
                'visual_concepts': self._generate_visual_concepts(trend),
                'copy_angles': self._generate_copy_angles(trend, brand_voice)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_integration_approach(self, trend: Dict[str, Any], 
                                 campaign_goal: str, 
                                 brand_voice: str) -> str:
        """Determine how to integrate trend based on campaign context"""
        
        if brand_voice == 'edgy':
            return f"Use {trend['title']} as a provocative hook that challenges conventional thinking"
        elif brand_voice == 'roast':
            return f"Playfully roast the absurdity of {trend['title']} while positioning your solution"
        elif brand_voice == 'professional':
            return f"Reference {trend['title']} as a cultural insight that validates your approach"
        else:
            return f"Cleverly incorporate {trend['title']} to create instant recognition and relatability"
    
    def _generate_content_ideas(self, trend: Dict[str, Any], 
                               campaign_goal: str, 
                               brand_voice: str) -> List[str]:
        """Generate specific content ideas using the trend"""
        
        ideas = [
            f"Create a {trend['type']} that shows your solution vs the trending problem",
            f"Use the {trend['title']} format to highlight your unique value proposition",
            f"Build a narrative around how your service addresses the underlying issue behind {trend['title']}"
        ]
        
        if trend['type'] == 'meme_format':
            ideas.append(f"Adapt the {trend['title']} meme template with your brand messaging")
        
        if trend['type'] == 'cultural_moment':
            ideas.append(f"Position your brand as understanding and solving the {trend['title']} frustration")
        
        return ideas
    
    def _generate_visual_concepts(self, trend: Dict[str, Any]) -> List[str]:
        """Generate visual concepts incorporating the trend"""
        
        concepts = [
            f"Visual recreation of {trend['title']} with your brand elements",
            f"Split-screen comparison using {trend['title']} as the 'before' state",
            f"Subtle nod to {trend['title']} in background or visual metaphor"
        ]
        
        if trend['platform'] == 'tiktok':
            concepts.append("Quick-cut video format matching TikTok native style")
        
        return concepts
    
    def _generate_copy_angles(self, trend: Dict[str, Any], brand_voice: str) -> List[str]:
        """Generate copy angles incorporating the trend"""
        
        base_angles = [
            f"We see you dealing with {trend['description']} - here's the real solution",
            f"Everyone's talking about {trend['title']}, but nobody's talking about this",
            f"While everyone's focused on {trend['title']}, smart people are doing this instead"
        ]
        
        if brand_voice == 'edgy':
            base_angles.append(f"Hot take: {trend['title']} is just a symptom of this bigger problem")
        elif brand_voice == 'roast':
            base_angles.append(f"POV: You're still dealing with {trend['title']} when this exists")
        
        return base_angles
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached trends are still valid"""
        
        if cache_key not in self._trend_cache:
            return False
        
        cache_time = self._trend_cache[cache_key]['timestamp']
        return (datetime.utcnow() - cache_time).seconds < self.cache_duration
    
    def _get_fallback_trends(self) -> List[Dict[str, Any]]:
        """Get fallback trends when discovery fails"""
        
        return [
            {
                'type': 'universal_trend',
                'title': 'Productivity overwhelm',
                'description': 'People feeling overwhelmed by productivity advice and tools',
                'engagement_score': 80,
                'relevance_score': 85,
                'platform': 'universal',
                'viral_factor': 'Everyone feels behind and overstimulated',
                'usage_tip': 'Position as the simple solution that actually works'
            }
        ]
    
    def _get_trend_sources(self) -> Dict[str, str]:
        """Get configuration for trend discovery sources"""
        
        return {
            'google_trends': 'https://trends.google.com/trends/api',
            'twitter_api': 'https://api.twitter.com/2/tweets/search',
            'reddit_api': 'https://www.reddit.com/r/all/hot.json',
            'tiktok_discover': 'https://www.tiktok.com/api/discover',
            'youtube_trends': 'https://www.googleapis.com/youtube/v3/videos'
        }