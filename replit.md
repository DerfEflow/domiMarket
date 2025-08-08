# Overview

"Dominate Marketing" is a comprehensive multi-tier Flask marketing platform that revolutionizes campaign creation through advanced AI technology. The platform features tier-based AI model access: Premium users (Pro/Enterprise) get GPT-4o, Google VEO 3, and Pika Labs, while lower tiers use GPT-4o-mini for cost savings. Claude Sonnet 4 handles quality assessment across all tiers. The system generates viral marketing campaigns with automated quality control, unlike traditional agencies stuck with outdated methods. Users authenticate via Google OAuth and receive complete marketing packages based on their subscription tier. The platform is production-ready with fully functional coupon system, database architecture, and payment integration.

## Recent System Updates (August 2025)
- **CRITICAL: Navigation & UX Fixes (August 8, 2025)**: Fixed all broken links, duplicate routes, and redundant buttons across the site
- **Landing Page Restored**: Reverted to original preferred aesthetic and wording while maintaining technical fixes  
- **Complete Route Stability**: All 7 main navigation routes (/, /features, /faq, /terms, /privacy, /auth/pricing, /auth/login) return 200 status codes
- **Removed Duplicate Route Conflicts**: Fixed server crashes caused by duplicate faq/features routes between app.py and main_app.py
- **Authentication Flow Cleanup**: All "Get Started" buttons now properly route to pricing page (no non-existent signup routes)
- **CRITICAL: Asynchronous Campaign Processing**: Implemented background job processing to prevent worker crashes and memory exhaustion during AI generation
- **Campaign Status Tracking**: Real-time status monitoring with auto-refreshing interface for users to track campaign progress  
- **Scalable Architecture**: Moved from synchronous to async processing to handle multiple concurrent users generating campaigns
- **Production-Ready Demo**: Fixed demo/live route with lightweight content that doesn't crash workers during intensive AI processing
- **Complete Workflow Integration**: End-to-end campaign generation workflow fully tested and functional
- **Google OAuth Authentication**: Configured for custom domain dominatemarketing.ninja - OAuth callback URL updated for production use
- **Custom Domain Integration**: Platform configured to work with dominatemarketing.ninja domain for Google OAuth compliance
- **Interactive Front Page Demo**: Replaced placeholder video with professional HTML5 Canvas animation showcasing AI workflow
- **Social Media Scheduling System**: Complete multi-platform posting and scheduling with OAuth integration
- **User-Specific Campaign Generation**: Every user gets completely fresh analysis and content generation from their input
- **No Static/Cached Content**: All campaigns start from scratch with fresh website analysis and viral research
- **Personal Data Flow**: User's business URL triggers fresh Sell Profile analysis → Viral Tools research → AI content generation → Quality validation
- **Individual Content Regeneration**: Users can regenerate specific content types (text, image, video) with feedback
- **Fresh Campaign Route**: New `/start-fresh-campaign` ensures no cached data influences user's results
- **Data Quality Improvements**: Enhanced Sell Profile analyzer with improved keyword extraction and location detection
- **Hidden Internal Methodology**: Removed extraction method details and priority systems from user interface
- **Actual AI Generation**: Implemented ContentGenerator service with real DALL-E image creation and GPT-4o text generation
- **Quality Agent Integration**: Claude Sonnet 4 validates all content for viral potential and brand alignment
- **Gallery Layout Redesign**: Clean responsive grid interface with clickable thumbnails for content inspection
- **Simplified Content Display**: Combined text/image and text/video formats instead of platform-specific versions
- **Tier-based AI Models**: Premium tiers use GPT-4o, Google VEO 3, Pika Labs; Standard tiers use GPT-4o-mini

## User Data Capture System (Latest)
- Comprehensive marketing data collection through profile completion forms
- Captures: contact info, business details, marketing budget, target audience, goals, and challenges
- GDPR-compliant consent management for email and SMS marketing
- Profile completion tracking with progress indicators and guided onboarding
- Marketing data export system for campaign targeting and lead management
- Automatic redirection to profile completion for new users

## Content Gallery & Social Media Integration (Latest)
- Comprehensive content gallery with filtering by videos, images, text, and scheduled posts
- Real-time content editing and regeneration capabilities for all media types
- Social media scheduling across Facebook, Instagram, X, TikTok, and LinkedIn
- Multi-platform posting with frequency options (once, daily, weekly, monthly)
- Content uniqueness enhancement system ensuring viral, data-driven campaigns
- Automated quality validation preventing generic agency copy

## Sell Profile → Viral Tools Methodology (Latest - January 2025)
- **Sell Profile Analyzer**: Extracts comprehensive business intelligence from websites
  - Business name, industry classification, geographic indicators, metadata extraction
  - About section analysis, company distinctives, and social media profile discovery
  - Intelligent fallback system for websites that block scrapers using URL-based analysis
  - Confidence scoring system for profile quality assessment

- **Viral Tools Researcher**: Discovers viral content opportunities in priority order
  - Priority 1: Industry-specific viral trends using Google Trends API and industry keyword mapping
  - Priority 2: Popular viral trends (general) including current social media formats
  - Priority 3: Viral memes with specific business application suggestions
  - Real-time trend analysis with authentic Google Trends data integration
  - Platform-specific content recommendations (TikTok, Instagram, Facebook, Twitter, LinkedIn)

## One-Click Media Licensing Generator (Latest - January 2025)
- Comprehensive licensing system with tier-based usage rights (Personal, Small Business, Professional, Enterprise)
- Automatic license document generation with unique IDs and legal terms
- Commercial use permissions, distribution rights, and modification rights based on subscription tier
- License verification system with API endpoints for validation
- Duration-based licensing (12-36 months or lifetime for Enterprise)
- Watermarked demo content with licensing integration showing upgrade paths
- Download and verification system for all generated licenses
- Professional legal document templates with GDPR compliance

# User Preferences

Preferred communication style: Simple, everyday language.
Platform Branding: "Dominate Marketing" with edgy, confident, exclusive copy without being arrogant
AI References: Use general AI terms instead of specific platform names to sound exclusive and cutting-edge
Key Messaging: Automatic trend implementation from 6-hour-old data vs outdated 20-year-old methods
Quality Focus: All content must pass quality assessment before delivery to users
Brand Voice Options: Standard voices plus new "edgy" (provocative, boundary-pushing) and "roast" (hilariously roasts market/competitors) tones

# System Architecture

## Frontend Architecture
The application uses a traditional server-side rendered architecture with Flask's Jinja2 templating engine. The frontend consists of:
- **Base Template System**: A modular template structure with `base.html` providing consistent layout and navigation
- **Bootstrap Integration**: Uses Replit's dark theme Bootstrap CSS for consistent styling across the platform
- **Form-Based Interface**: Single-page form collection with validation and flash messaging
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

## Backend Architecture
The Flask application follows a simple MVC pattern:
- **Route Handlers**: Minimal controllers handling form submission and data validation
- **File-Based Storage**: JSON files stored in an `outputs` directory structure organized by job IDs
- **Session Management**: Flash messaging for user feedback using Flask's session system
- **Error Handling**: Basic form validation with user-friendly error messages

## Data Storage Architecture
The system uses a file-based storage approach rather than a traditional database:
- **JSON Format**: Campaign data stored as structured JSON files
- **Directory Structure**: Organized by unique job IDs (`/outputs/<job_id>/`)
- **UUID Generation**: Each campaign gets a unique identifier for tracking and organization
- **Timestamp Tracking**: ISO format timestamps for data creation tracking

## User-Specific Processing Pipeline Design
The application implements a completely fresh, user-specific AI-powered processing pipeline for each campaign using asynchronous background processing:
1. **User Input Collection**: Web form captures user's business URL, audience, and campaign goals
2. **Async Job Submission**: Campaign generation submitted to background queue with immediate job ID return
3. **Real-Time Status Tracking**: Users monitor campaign progress through status page with auto-refresh
4. **Fresh Website Analysis**: SellProfileAnalyzer analyzes user's specific business URL in background thread
5. **Real-Time Viral Research**: ViralToolsResearcher discovers trends based on user's business intelligence
6. **User-Specific Content Generation**: ContentGenerator creates unique AI content for user's business only
7. **Individual Quality Assessment**: QualityAgent validates user's specific content for viral potential
8. **Personal Campaign Storage**: User's campaign saved with their unique data (no shared content)
9. **Individual Regeneration**: Users can regenerate specific content types with personal feedback
10. **Fresh Campaign Restart**: `/start-fresh-campaign` clears all cached data for clean user experience
11. **Tier-Based AI Models**: User's subscription tier determines AI models used (GPT-4o vs GPT-4o-mini)
12. **Personal Content Gallery**: User-specific content display with regeneration capabilities
13. **User Analytics**: Personal campaign performance tracking and analytics dashboard
14. **Background Processing**: All intensive AI operations run in worker threads to prevent request timeouts

## Integration Architecture
The system is built to support future integrations with:
- **Advanced AI APIs**: For generating ad scripts and voiceover content
- **Professional Video Generation**: Next-generation AI video creation capabilities
- **Business Data Scraping**: URL-based business information extraction
- **Media Asset Management**: Logo and visual asset handling

# External Dependencies

## Core Framework Dependencies
- **Flask**: Python web framework providing routing, templating, and session management
- **Python Standard Library**: UUID generation, JSON handling, datetime operations, and logging
- **AI Integration SDKs**: Professional AI APIs for text and video generation
- **Advanced AI Models**: Next-generation language and multimedia AI capabilities

## Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework with Replit's dark theme customization
- **Font Awesome 6.4.0**: Icon library for enhanced user interface elements
- **CDN-Based Delivery**: All frontend assets loaded via CDN for reliability and performance

## Active AI Integrations
- **OpenAI GPT-5/GPT-5-mini**: Tier-based text content generation, image prompts, and video scripts
- **Google VEO 3**: Professional video generation from AI scripts (Pro tier and above)
- **Pika Labs**: Image-to-video animation and enhancement (Enterprise tier exclusive)
- **Claude Sonnet 4**: Quality assessment agent ensuring viral content standards across all tiers
- **Campaign Orchestrator**: Coordinates all AI services with tier-appropriate model selection
- **Automated Quality Control**: All content passes through Claude assessment before delivery

## Development Environment
- **Replit Platform**: Cloud-based development and hosting environment
- **Environment Variables**: Session secrets and API keys managed through environment configuration
- **File System**: Local file storage for outputs and static assets

## Runtime Dependencies
- **Python 3.x**: Core runtime environment
- **WSGI Server**: Production deployment capability through standard WSGI interface
- **Static Asset Serving**: Flask's built-in static file serving for CSS and other assets