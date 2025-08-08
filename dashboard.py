from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response, session
from flask_login import login_required, current_user
from models import Campaign, Competitor, SocialAccount, Brand, db, SubscriptionTier
from services.campaign_orchestrator import CampaignOrchestrator
from services.ai_models import ModelConfig
# Import services with fallbacks for missing modules
scrape_business_data = None
analyze_competitors = None
get_industry_trends = None
generate_marketing_theme = None
generate_ad_content = None
create_veo_prompt = None
generate_video_with_veo3 = None
AIProcessor = None
DataExporter = None
FormValidator = None
FileValidator = None

try:
    from services.web_scraper import scrape_business_data
except ImportError:
    pass

try:
    from services.competitor_analysis import analyze_competitors, get_industry_trends
except ImportError:
    pass

try:
    from services.creative_ai import generate_marketing_theme, generate_ad_content, create_veo_prompt
except ImportError:
    pass

try:
    from services.veo_client import generate_video_with_veo3
except ImportError:
    pass

try:
    from services.ai_processor import AIProcessor, DataExporter
except ImportError:
    pass

try:
    from services.form_validator import FormValidator, FileValidator
except ImportError:
    pass
import json
import uuid
from datetime import datetime
import logging
import os

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    """Main dashboard"""
    campaigns = Campaign.query.filter_by(user_id=current_user.id).order_by(Campaign.created_at.desc()).limit(10).all()
    return render_template('dashboard/index.html', campaigns=campaigns)

@dashboard.route('/demo')
def demo_preview():
    """Demo preview page for proof-of-capability"""
    demo_results = session.get('demo_results')
    return render_template('demo/preview.html', demo_results=demo_results)

@dashboard.route('/demo/live')
def demo_live():
    """Live demo page with lightweight demonstration"""
    # Use lightweight demo data that doesn't crash workers
    demo_data = {
        'company': {'name': 'Truline Roofing', 'url': 'https://trulineroofing.com'},
        'sell_profile': {
            'business_name': 'Truline Roofing', 
            'industry': 'construction', 
            'confidence_score': 0.90,
            'keywords': ['roofing', 'repair', 'restoration', 'commercial'],
            'geography': {'state': 'North Carolina', 'cities': ['Charlotte', 'Raleigh'], 'country': 'USA'},
            'distinctives': ['24/7 Emergency Service', '20+ Years Experience', 'Licensed & Insured']
        },
        'viral_tools': {
            'industry_trends': [
                {'trend': 'Digital transformation in construction', 'relevance': 0.85},
                {'trend': 'Sustainable building practices', 'relevance': 0.78},
                {'trend': 'Emergency response marketing', 'relevance': 0.92}
            ],
            'popular_viral_trends': [
                {'platform': 'TikTok', 'format': 'Before/after transformation videos'},
                {'platform': 'Instagram', 'format': 'Time-lapse project completion'},
                {'platform': 'Facebook', 'format': 'Customer testimonial stories'}
            ],
            'viral_memes': [
                {'meme': 'Expectations vs Reality', 'application': 'Show quality roofing results'},
                {'meme': 'This is Fine', 'application': 'Emergency roof repair humor'},
                {'meme': 'Drake Pointing', 'application': 'Old roof vs new roof comparison'}
            ],
            'confidence_score': 0.88
        },
        'generated_content': {
            'text_content': [
                {'content': '🏠 When your roof is giving you trust issues, Truline delivers certainty. 20+ years of making North Carolina homes weatherproof across Charlotte and Raleigh. #RoofingDoneRight', 'viral_trend_applied': 'Trust & reliability messaging', 'id': 'text1'},
                {'content': 'POV: You called Truline at 2 AM for emergency roofing and they actually answered 📞 Some heroes don\'t wear capes... they wear hard hats. #EmergencyRoofing', 'viral_trend_applied': 'POV trend with emergency service', 'id': 'text2'},
                {'content': 'Expectation: "It\'s just a small leak"\nReality: *shows massive water damage*\nSolution: Truline Roofing - We fix it before it becomes a disaster 🔧', 'viral_trend_applied': 'Expectation vs Reality meme', 'id': 'text3'}
            ],
            'image_content': [
                {'prompt': 'Professional roofing crew working on modern home with storm clouds in background, dramatic lighting', 'url': '/static/demo-roof-1.jpg', 'id': 'img1'},
                {'prompt': 'Before and after split image: damaged shingles vs pristine new roof installation', 'url': '/static/demo-roof-2.jpg', 'id': 'img2'},
                {'prompt': 'Emergency roofing response truck arriving at house during storm, heroic composition', 'url': '/static/demo-roof-3.jpg', 'id': 'img3'}
            ],
            'video_content': [
                {'script': 'Time-lapse of complete roof transformation: "From disaster to dream home in 48 hours. Truline Roofing - Because your family deserves better."', 'url': '/static/demo-video-1.mp4', 'prompt': 'Time-lapse roof transformation', 'duration': '30s', 'resolution': '4K'},
                {'script': 'Customer testimonial: "I called 5 companies. Only Truline answered at midnight. Roof fixed by morning. Real heroes exist." #TrulineTestimonial', 'url': '/static/demo-video-2.mp4', 'prompt': 'Customer testimonial video', 'duration': '45s', 'resolution': 'HD'}
            ],
            'combined_content': [
                {'text_content': 'When Mother Nature tests your roof, make sure it passes. ✅ Truline Roofing - North Carolina\'s weather warriors serving Charlotte and Raleigh.', 'image': 'Storm-resistant roof installation', 'platform': 'Multi-platform', 'type': 'text_image', 'id': 'combo1'},
                {'text_content': 'Your roof protects everything you love. We protect your roof. Simple math. 🏠❤️', 'image': 'Family home with perfect roofing', 'platform': 'Family-focused marketing', 'type': 'text_image', 'id': 'combo2'}
            ]
        },
        'quality_validation': {
            'overall_score': 92,
            'feedback': 'Excellent viral potential with strong local appeal and emergency service differentiation',
            'viral_elements': ['Emergency response angle', 'Local Ohio focus', 'Trust and reliability', 'Visual transformation content'],
            'improvements': ['Add more seasonal content', 'Include warranty messaging', 'Expand service area coverage']
        },
        'generation_metadata': {
            'generated_at': datetime.now().isoformat(),
            'ai_models_used': ['GPT-4o', 'DALL-E 3', 'Claude Sonnet 4'],
            'processing_time': '2.3 seconds',
            'content_pieces': 12
        }
    }
    
    return render_template('demo_live_redesigned.html', demo_data=demo_data)

@dashboard.route('/demo/analysis', methods=['POST'])
def demo_analysis():
    """Process demo analysis request"""
    try:
        from services.trends_collector import TrendsCollector
        from services.ai_content_generator import AIContentGenerator
        trends_collector = TrendsCollector()
        ai_generator = AIContentGenerator()
    except ImportError as e:
        logging.warning(f"Could not import AI services: {e}")
        trends_collector = None
        ai_generator = None
        ai_generator = None
    
    website_url = request.form.get('website_url', 'https://stripe.com')
    industry = request.form.get('industry', 'technology')
    include_trends = 'include_trends' in request.form
    competitor_analysis = 'competitor_analysis' in request.form
    
    # Create demo results data based on form inputs
    demo_results = {
        'website_url': website_url,
        'industry': industry,
        'include_trends': include_trends,
        'competitor_analysis': competitor_analysis,
        'business_analysis': {
            'company_name': 'Sample Business',
            'description': 'Innovative technology platform providing cutting-edge solutions',
            'target_audience': 'Tech-savvy professionals and businesses',
            'key_strengths': ['Strong online presence', 'Clear value proposition', 'Modern tech stack']
        },
        'competitors': [
            {'name': 'PayPal', 'strength': 'Brand recognition', 'weakness': 'Complex pricing'},
            {'name': 'Square', 'strength': 'SMB focus', 'weakness': 'Limited international'},
            {'name': 'Adyen', 'strength': 'Enterprise features', 'weakness': 'High complexity'}
        ] if competitor_analysis else [],
        'viral_trends': [],
        'ad_content': {
            'headline': f'Transform Your {industry.title()} Business Today',
            'description': 'Join thousands of companies already using cutting-edge solutions to dominate their market',
            'cta': 'Start Your Free Trial'
        }
    }
    
    # Generate viral trends if requested
    if include_trends and trends_collector:
        try:
            # Get real viral trends from the collector
            current_trends = trends_collector.get_top_viral_trends(8)
            viral_trends = [trend['topic'].replace('_', ' ').title() for trend in current_trends if trend['relevance'] in ['high', 'medium']]
            
            # Fallback to sample trends if no real trends found
            if not viral_trends:
                viral_trends = [
                    "AI automation buzz", 
                    "Sustainable business wave", 
                    "Remote work revolution",
                    "Personalization trend",
                    "Data-driven momentum"
                ]
            demo_results['viral_trends'] = viral_trends[:5]  # Limit to 5 trends
        except Exception as e:
            # Fallback trends if collector fails
            demo_results['viral_trends'] = [
                "Current market disruption", 
                "Digital transformation wave", 
                "Customer-first movement",
                "Innovation acceleration",
                "Growth optimization trend"
            ]
    elif include_trends:
        # Fallback when trends collector not available
        demo_results['viral_trends'] = [
            "AI automation tools", 
            "Sustainable business practices", 
            "Remote work optimization",
            "Customer experience personalization",
            "Data-driven decision making"
        ]
    
    # Generate real AI content if available
    if ai_generator:
        try:
            business_name = demo_results['business_analysis']['company_name']
            
            # Generate marketing image with watermark
            logging.info(f"Generating AI image for {business_name}")
            image_result = ai_generator.generate_marketing_image(business_name, industry, "product showcase")
            if image_result.get('success'):
                demo_results['ai_image'] = image_result
            
            # Generate video concept with watermark
            logging.info(f"Generating video concept for {business_name}")
            video_result = ai_generator.generate_marketing_video_concept(business_name, industry)
            if video_result.get('success'):
                demo_results['ai_video'] = video_result
            
            # Generate social media posts
            logging.info(f"Generating social media posts for {business_name}")
            social_result = ai_generator.generate_social_media_posts(
                business_name, industry,
                demo_results.get('ai_image', {}).get('success', False),
                demo_results.get('ai_video', {}).get('success', False)
            )
            if social_result.get('success'):
                demo_results['social_posts'] = social_result
                
        except Exception as e:
            logging.error(f"Error generating AI content: {e}")
            # Add fallback indicators
            demo_results['ai_content_error'] = str(e)
    
    # Store demo results in session for display
    session['demo_results'] = demo_results
    flash(f'✅ Demo analysis complete! See your sample results below. Sign up to analyze your actual business.', 'success')
    return redirect(url_for('dashboard.demo_preview'))

@dashboard.route('/create-campaign')
@login_required
def create_campaign():
    """Campaign creation form"""
    return render_template('dashboard/create_campaign.html')

@dashboard.route('/create-campaign', methods=['POST'])
@login_required
def create_campaign_post():
    """Process campaign creation asynchronously to prevent worker crashes"""
    try:
        # Get form data
        business_url = request.form.get('business_url', '').strip()
        title = request.form.get('title', '').strip()
        target_audience = request.form.get('target_audience', '').strip()
        campaign_goal = request.form.get('campaign_goal', 'leads')
        brand_voice = request.form.get('brand_voice', 'professional')
        
        # Basic validation
        if not business_url:
            flash('Business URL is required', 'error')
            return redirect(url_for('dashboard.create_campaign'))
        
        # Get user's subscription tier
        user_tier = current_user.subscription_tier
        
        # Prepare campaign parameters for async processing
        campaign_params = {
            'campaign_goal': campaign_goal,
            'target_audience': target_audience,
            'brand_voice': brand_voice,
            'title': title,
            'tier': user_tier.value
        }
        
        # Submit job to async processor instead of processing immediately
        from services.async_campaign_processor import AsyncCampaignProcessor
        processor = AsyncCampaignProcessor()
        job_id = processor.submit_job(
            business_url=business_url,
            target_audience=target_audience,
            campaign_goal=campaign_goal,
            user_id=str(current_user.id),
            campaign_params=campaign_params
        )
        
        # Create campaign record in pending state
        campaign = Campaign()
        campaign.user_id = current_user.id
        campaign.title = title or f"Fresh Campaign for {business_url}"
        campaign.business_url = business_url
        campaign.target_audience = target_audience
        campaign.campaign_goal = campaign_goal
        campaign.status = 'processing'
        campaign.id = job_id  # Set job_id as campaign_id after creation
        db.session.add(campaign)
        db.session.commit()
        
        flash('Campaign generation started! You\'ll be notified when it\'s complete. This typically takes 2-3 minutes.', 'info')
        return redirect(url_for('dashboard.campaign_status', campaign_id=job_id))
        
        # Save campaign result to database
        if campaign_result.get('success'):
            # Create campaign record with user's fresh data
            campaign = Campaign(
                id=campaign_result['campaign_id'],
                user_id=current_user.id,
                title=title or f"Fresh Campaign for {business_url}",
                business_url=business_url,
                target_audience=target_audience,
                campaign_goal=campaign_goal,
                status=campaign_result.get('status', 'completed'),
                ai_content=json.dumps(campaign_result.get('content', {})),
                quality_score=campaign_result.get('quality_assessment', {}).get('overall_score', 85),
                tier_used=user_tier.value,
                services_used=json.dumps(campaign_result.get('services_used', []))
            )
            db.session.add(campaign)
            db.session.commit()
            
            if campaign_result.get('status') == 'completed':
                flash(f'Campaign created successfully using {user_tier.value} tier AI models!', 'success')
            elif campaign_result.get('status') == 'needs_revision':
                flash('Campaign created but needs revision based on quality assessment.', 'warning')
            
            return redirect(url_for('dashboard.view_campaign', campaign_id=campaign.id))
        else:
            # Handle errors
            error_messages = campaign_result.get('errors', ['Unknown error occurred'])
            for error in error_messages:
                flash(f'AI Processing Error: {error}', 'error')
            
            # Still create a failed campaign record for debugging
            campaign = Campaign(
                id=str(uuid.uuid4()),
                user_id=current_user.id,
                title=title or f"Failed Fresh Campaign for {business_url}",
                business_url=business_url,
                target_audience=target_audience,
                campaign_goal=campaign_goal,
                status='failed',
                ai_content=json.dumps(campaign_result),
                tier_used=user_tier.value
            )
            db.session.add(campaign)
            db.session.commit()
            
            return redirect(url_for('dashboard.view_campaign', campaign_id=campaign.id))
        
    except Exception as e:
        flash(f'Error creating campaign: {str(e)}', 'error')
        return redirect(url_for('dashboard.create_campaign'))

@dashboard.route('/ai-services-status')
@login_required
def ai_services_status():
    """Show AI services status and tier capabilities"""
    try:
        from services.ai_models import AIProvider
        orchestrator = CampaignOrchestrator()
        
        # Get tier information
        user_tier = current_user.subscription_tier
        capabilities = ModelConfig.get_tier_capabilities(user_tier)
        tier_models = {
            'openai': ModelConfig.get_model_for_tier(AIProvider.OPENAI, user_tier),
            'google_veo': ModelConfig.get_model_for_tier(AIProvider.GOOGLE_VEO, user_tier),
            'pika_labs': ModelConfig.get_model_for_tier(AIProvider.PIKA_LABS, user_tier),
            'quality_agent': ModelConfig.get_model_for_tier(AIProvider.CLAUDE, user_tier)
        }
        
        # Get service status
        service_status = orchestrator.get_service_status()
        
        # Get processing time estimate
        processing_estimate = orchestrator.estimate_processing_time(user_tier)
        
        # Set tier color for badge
        tier_colors = {
            'basic': 'secondary',
            'plus': 'info', 
            'pro': 'warning',
            'enterprise': 'success'
        }
        tier_color = tier_colors.get(user_tier.value, 'secondary')
        
        return render_template('dashboard/ai_services_status.html',
                             capabilities=capabilities,
                             tier_models=tier_models,
                             service_status=service_status,
                             processing_estimate=processing_estimate,
                             tier_color=tier_color)
    
    except Exception as e:
        flash(f'Error loading AI services status: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@dashboard.route('/tier-features')
@login_required  
def tier_features():
    """Show tier features and AI model comparison"""
    user_tier = current_user.subscription_tier
    tier_colors = {
        'basic': 'secondary',
        'plus': 'info', 
        'pro': 'warning',
        'enterprise': 'success'
    }
    tier_color = tier_colors.get(user_tier.value, 'secondary')
    
    return render_template('dashboard/tier_features.html', tier_color=tier_color)

@dashboard.route('/tone-examples')
@login_required
def tone_examples():
    """Show brand voice and tone examples"""
    return render_template('dashboard/tone_examples.html')

@dashboard.route('/regenerate-content/<campaign_id>', methods=['POST'])
@login_required
def regenerate_content(campaign_id):
    """Regenerate specific content for user's campaign based on their feedback"""
    try:
        # Get user's campaign
        campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
        if not campaign:
            flash('Campaign not found', 'error')
            return redirect(url_for('dashboard.campaigns'))
        
        # Get regeneration request details
        content_type = request.form.get('content_type')  # 'text', 'image', 'video'
        user_feedback = request.form.get('feedback', '')
        
        # Use fresh user campaign generator for regeneration
        try:
            from services.user_campaign_generator import UserCampaignGenerator
            user_generator = UserCampaignGenerator()
        except ImportError:
            flash('Campaign regeneration service not available', 'error')
            return redirect(url_for('dashboard.view_campaign', campaign_id=campaign_id))
        
        # Parse existing campaign data
        campaign_data = json.loads(campaign.ai_content) if campaign.ai_content else {}
        
        # Generate fresh content based on user feedback
        if content_type:
            regeneration_result = user_generator.regenerate_specific_content(
                campaign_data, content_type, user_feedback
            )
        else:
            flash('Content type is required for regeneration', 'error')
            return redirect(url_for('dashboard.view_campaign', campaign_id=campaign_id))
        
        if regeneration_result.get('success'):
            # Update campaign with fresh content
            campaign_data[f'regenerated_{content_type}'] = regeneration_result
            campaign.ai_content = json.dumps(campaign_data)
            campaign.updated_at = datetime.now()
            db.session.commit()
            
            flash(f'Fresh {content_type} content generated based on your feedback!', 'success')
        else:
            flash(f'Error regenerating {content_type}: {regeneration_result.get("error")}', 'error')
        
        return redirect(url_for('dashboard.view_campaign', campaign_id=campaign_id))
        
    except Exception as e:
        flash(f'Error processing regeneration: {str(e)}', 'error')
        return redirect(url_for('dashboard.view_campaign', campaign_id=campaign_id))

@dashboard.route('/campaign-status/<campaign_id>')
@login_required
def campaign_status(campaign_id):
    """Show campaign generation status and results when ready"""
    try:
        # Get campaign from database
        campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
        if not campaign:
            flash('Campaign not found', 'error')
            return redirect(url_for('dashboard.index'))
        
        # Check async processing status
        from services.async_campaign_processor import campaign_processor
        job_status = campaign_processor.get_job_status(campaign_id)
        
        if job_status['status'] == 'completed':
            # Update campaign with completed results
            campaign.status = 'completed'
            campaign.ai_content = json.dumps(job_status['data'])
            campaign.quality_score = job_status['data'].get('quality_validation', {}).get('overall_score', 85)
            db.session.commit()
            
            return redirect(url_for('dashboard.view_campaign', campaign_id=campaign_id))
        
        elif job_status['status'] == 'failed':
            # Update campaign with error status
            campaign.status = 'failed'
            db.session.commit()
            
            flash(f'Campaign generation failed: {job_status.get("error", "Unknown error")}', 'error')
            return redirect(url_for('dashboard.create_campaign'))
        
        # Still processing - show status page
        return render_template('dashboard/campaign_status.html', 
                             campaign=campaign, 
                             job_status=job_status)
        
    except Exception as e:
        flash(f'Error checking campaign status: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@dashboard.route('/start-fresh-campaign')
@login_required
def start_fresh_campaign():
    """Start completely fresh campaign generation for user"""
    # Clear any cached or previous data
    session.pop('demo_results', None)
    flash('Starting fresh campaign generation. All content will be generated specifically for your business.', 'info')
    return redirect(url_for('dashboard.create_campaign'))

@dashboard.route('/gallery')
@login_required
def gallery():
    """Content gallery and management"""
    from models import Campaign, SocialPost
    
    # Get user's campaigns
    campaigns = Campaign.query.filter_by(user_id=current_user.id).order_by(Campaign.created_at.desc()).all()
    
    # Get scheduled posts
    scheduled_posts = SocialPost.query.filter_by(
        user_id=current_user.id, 
        status='scheduled'
    ).order_by(SocialPost.scheduled_time.asc()).all()
    
    return render_template('dashboard/gallery.html', campaigns=campaigns, scheduled_posts=scheduled_posts)

@dashboard.route('/campaigns/<campaign_id>/edit')
@login_required
def edit_campaign_data(campaign_id):
    """Get campaign data for editing"""
    from models import Campaign
    import json
    
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    return jsonify({
        'title': campaign.title,
        'ad_text': campaign.ad_text,
        'image_prompt': campaign.image_prompt,
        'business_url': campaign.business_url,
        'target_audience': campaign.target_audience,
        'campaign_goal': campaign.campaign_goal,
        'brand_voice': campaign.brand_voice
    })

@dashboard.route('/campaigns/<campaign_id>/update', methods=['POST'])
@login_required
def update_campaign(campaign_id):
    """Update campaign content"""
    from models import Campaign
    from main_app import db
    
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    try:
        campaign.title = request.form.get('title', campaign.title)
        campaign.ad_text = request.form.get('ad_text', campaign.ad_text)
        campaign.image_prompt = request.form.get('image_prompt', campaign.image_prompt)
        
        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/campaigns/<campaign_id>/update-business-data', methods=['POST'])
@login_required
def update_business_data(campaign_id):
    """Update business analysis data for campaign"""
    from models import Campaign
    from main_app import db
    import json
    
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    try:
        # Parse existing business metadata or create new
        business_metadata = json.loads(campaign.business_metadata) if campaign.business_metadata else {}
        
        # Update with form data
        business_metadata.update({
            'title': request.form.get('business_name', '').strip(),
            'industry': request.form.get('industry', '').strip(),
            'description': request.form.get('description', '').strip(),
            'location': {
                'state': request.form.get('state', '').strip(),
                'cities': [city.strip() for city in request.form.get('cities', '').split(',') if city.strip()]
            },
            'keywords': [keyword.strip() for keyword in request.form.get('keywords', '').split(',') if keyword.strip()],
            'distinctives': [distinctive.strip() for distinctive in request.form.get('distinctives', '').split('\n') if distinctive.strip()]
        })
        
        # Save updated metadata
        campaign.business_metadata = json.dumps(business_metadata)
        campaign.updated_at = datetime.now()
        db.session.commit()
        
        flash('Business data updated successfully!', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/social-scheduling')
@login_required
def social_scheduling():
    """Social media scheduling dashboard"""
    from models import SocialPost, SocialAccount, Campaign
    from services.social_media_integration import SocialMediaService
    from app import db
    from datetime import datetime, timedelta
    
    try:
        social_service = SocialMediaService()
        
        # Get user's connected social accounts
        connected_accounts = social_service.get_user_accounts(str(current_user.id))
        social_accounts = {}
        for account in connected_accounts:
            social_accounts[account.platform] = account
        
        # Get user's campaigns for scheduling
        user_campaigns = Campaign.query.filter_by(user_id=current_user.id, status='completed').limit(20).all()
        
        # Get scheduled posts
        scheduled_posts = SocialPost.query.filter_by(user_id=current_user.id).order_by(SocialPost.scheduled_time.desc()).limit(50).all()
        
        # Calculate stats
        stats = {
            'scheduled': SocialPost.query.filter_by(user_id=current_user.id, status='scheduled').count(),
            'posted': SocialPost.query.filter_by(user_id=current_user.id, status='posted').count(),
            'failed': SocialPost.query.filter_by(user_id=current_user.id, status='failed').count(),
            'recurring': SocialPost.query.filter_by(user_id=current_user.id, is_recurring=True).count()
        }
        
        return render_template('dashboard/social_scheduling.html',
                             social_accounts=social_accounts,
                             user_campaigns=user_campaigns,
                             scheduled_posts=scheduled_posts,
                             stats=stats)
    
    except Exception as e:
        flash(f'Error loading social scheduling: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@dashboard.route('/schedule-post', methods=['POST'])
@login_required
def schedule_post():
    """Schedule social media posts"""
    from models import Campaign, SocialPost
    from app import db
    import json
    from datetime import datetime
    
    try:
        campaign_id = request.form.get('campaign_id')
        platforms = json.loads(request.form.get('platforms', '[]'))
        schedule_datetime = request.form.get('schedule_datetime')
        frequency = request.form.get('frequency', 'once')
        custom_content = request.form.get('content', '')
        
        campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        schedule_dt = datetime.fromisoformat(schedule_datetime) if schedule_datetime else datetime.now()
        
        # Create scheduled posts for each platform
        for platform in platforms:
            post = SocialPost()
            post.user_id = current_user.id
            post.campaign_id = campaign_id
            post.platform = platform
            post.content = custom_content if custom_content else campaign.ad_text or 'Your viral marketing campaign is ready!'
            post.scheduled_time = schedule_dt
            post.post_frequency = frequency
            post.is_recurring = frequency != 'once'
            post.status = 'scheduled'
            
            # Add media URLs if available
            if campaign.image_path:
                post.image_url = campaign.image_path
            if campaign.video_path:
                post.video_url = campaign.video_path
            
            db.session.add(post)
        
        db.session.commit()
        flash(f'Posts scheduled for {len(platforms)} platforms!', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/campaign/<campaign_id>/content')
@login_required
def get_campaign_content(campaign_id):
    """Get campaign content for scheduling"""
    from models import Campaign
    
    try:
        campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        # Get AI-generated content
        ai_content = json.loads(campaign.ai_content) if campaign.ai_content else {}
        text_content = ai_content.get('text_content', [])
        
        # Use the first text content or fallback
        content = text_content[0] if text_content else campaign.ad_text or 'Your viral marketing campaign is ready!'
        
        return jsonify({
            'success': True,
            'content': content,
            'media': {
                'image': campaign.image_path,
                'video': campaign.video_path
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/social/post-now/<post_id>', methods=['POST'])
@login_required
def post_now(post_id):
    """Post immediately"""
    from models import SocialPost
    from services.social_media_integration import SocialMediaService
    from app import db
    
    try:
        post = SocialPost.query.filter_by(id=post_id, user_id=current_user.id).first()
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        social_service = SocialMediaService()
        result = social_service.post_to_platform(post)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/social/cancel/<post_id>', methods=['POST'])
@login_required
def cancel_post(post_id):
    """Cancel scheduled post"""
    from models import SocialPost
    from app import db
    
    try:
        post = SocialPost.query.filter_by(id=post_id, user_id=current_user.id).first()
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        post.status = 'cancelled'
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/social/retry/<post_id>', methods=['POST'])
@login_required
def retry_post(post_id):
    """Retry failed post"""
    from models import SocialPost
    from services.social_media_integration import SocialMediaService
    from app import db
    
    try:
        post = SocialPost.query.filter_by(id=post_id, user_id=current_user.id).first()
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        post.status = 'scheduled'
        post.error_message = None
        db.session.commit()
        
        social_service = SocialMediaService()
        result = social_service.post_to_platform(post)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/social/disconnect/<platform>', methods=['POST'])
@login_required
def disconnect_social_account(platform):
    """Disconnect social media account"""
    from models import SocialAccount
    from app import db
    
    try:
        account = SocialAccount.query.filter_by(
            user_id=current_user.id,
            platform=platform,
            is_active=True
        ).first()
        
        if account:
            account.is_active = False
            db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/campaigns/<campaign_id>/regenerate-video', methods=['POST'])
@login_required
def regenerate_video(campaign_id):
    """Regenerate video content for campaign"""
    from models import Campaign
    from services.campaign_orchestrator import CampaignOrchestrator
    
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    try:
        # Check if user's tier supports video generation
        capabilities = ModelConfig.get_tier_capabilities(current_user.subscription_tier)
        if not capabilities.get('video_generation', False):
            return jsonify({'error': 'Video generation not available for your tier'}), 403
        
        orchestrator = CampaignOrchestrator()
        
        # Regenerate video using existing campaign data
        business_data = {
            'business_url': campaign.business_url,
            'description': campaign.business_metadata.get('description', '') if campaign.business_metadata else '',
            'industry': campaign.business_metadata.get('industry', '') if campaign.business_metadata else ''
        }
        
        video_result = orchestrator.generate_video_content(
            business_data=business_data,
            subscription_tier=current_user.subscription_tier,
            campaign_goal=campaign.campaign_goal,
            target_audience=campaign.target_audience,
            brand_voice=campaign.brand_voice
        )
        
        if video_result.get('success'):
            campaign.video_path = video_result.get('video_path')
            campaign.video_prompt = video_result.get('video_prompt')
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to regenerate video'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/campaigns/<campaign_id>/regenerate-image', methods=['POST'])
@login_required
def regenerate_image(campaign_id):
    """Regenerate image content for campaign"""
    from models import Campaign
    from services.campaign_orchestrator import CampaignOrchestrator
    
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    try:
        # Check if user's tier supports image generation
        capabilities = ModelConfig.get_tier_capabilities(current_user.subscription_tier)
        if not capabilities.get('image_generation', False):
            return jsonify({'error': 'Image generation not available for your tier'}), 403
        
        orchestrator = CampaignOrchestrator()
        
        # Regenerate image using existing campaign data
        business_data = {
            'business_url': campaign.business_url,
            'description': campaign.business_metadata.get('description', '') if campaign.business_metadata else '',
            'industry': campaign.business_metadata.get('industry', '') if campaign.business_metadata else ''
        }
        
        image_result = orchestrator.generate_image_content(
            business_data=business_data,
            subscription_tier=current_user.subscription_tier,
            campaign_goal=campaign.campaign_goal,
            target_audience=campaign.target_audience,
            brand_voice=campaign.brand_voice
        )
        
        if image_result.get('success'):
            campaign.image_path = image_result.get('image_path')
            campaign.image_prompt = image_result.get('image_prompt')
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to regenerate image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/campaigns/<campaign_id>/regenerate-text', methods=['POST'])
@login_required
def regenerate_text(campaign_id):
    """Regenerate text content for campaign"""
    from models import Campaign
    from services.campaign_orchestrator import CampaignOrchestrator
    
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    try:
        orchestrator = CampaignOrchestrator()
        
        # Regenerate text using existing campaign data
        business_data = {
            'business_url': campaign.business_url,
            'description': campaign.business_metadata.get('description', '') if campaign.business_metadata else '',
            'industry': campaign.business_metadata.get('industry', '') if campaign.business_metadata else ''
        }
        
        text_result = orchestrator.generate_text_content(
            business_data=business_data,
            subscription_tier=current_user.subscription_tier,
            campaign_goal=campaign.campaign_goal,
            target_audience=campaign.target_audience,
            brand_voice=campaign.brand_voice
        )
        
        if text_result.get('success'):
            campaign.ad_text = text_result.get('ad_text')
            campaign.marketing_theme = text_result.get('marketing_theme')
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to regenerate text'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/social-media')
@login_required
def social_media_accounts():
    """Social media accounts management"""
    from models import SocialAccount
    
    # Get user's connected accounts
    connected_accounts = SocialAccount.query.filter_by(
        user_id=current_user.id, 
        is_active=True
    ).all()
    
    # Check which platforms are connected
    platform_status = {
        'facebook_connected': any(acc.platform == 'facebook' for acc in connected_accounts),
        'instagram_connected': any(acc.platform == 'instagram' for acc in connected_accounts),
        'twitter_connected': any(acc.platform == 'twitter' for acc in connected_accounts),
        'tiktok_connected': any(acc.platform == 'tiktok' for acc in connected_accounts),
        'linkedin_connected': any(acc.platform == 'linkedin' for acc in connected_accounts),
    }
    
    # Get usernames for connected accounts
    for account in connected_accounts:
        platform_status[f'{account.platform}_username'] = account.username
    
    return render_template('dashboard/social_accounts.html', 
                         connected_accounts=connected_accounts, 
                         **platform_status)

@dashboard.route('/process-campaign/<campaign_id>')
@login_required
def process_campaign(campaign_id):
    """Process campaign with AI analysis"""
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('dashboard.index'))
    
    try:
        # Step 1: Scrape business website
        flash('Analyzing your website...', 'info')
        if 'scrape_business_data' in globals():
            business_data = scrape_business_data(campaign.business_url)
        else:
            business_data = {'error': 'Business data scraper not available'}
        campaign.business_metadata = business_data
        
        # Step 2: Analyze competitors (Pro tier and above)
        competitor_insights = {}
        if current_user.can_access_tier(SubscriptionTier.PRO):
            flash('Analyzing your competitors...', 'info')
            if 'analyze_competitors' in globals():
                competitor_analysis = analyze_competitors(
                    campaign.business_url, 
                    business_data, 
                    current_user.industry
                )
            else:
                competitor_analysis = {'competitors': [], 'insights': {}}
            
            # Save competitors to database
            for comp in competitor_analysis.get('competitors', []):
                existing = Competitor.query.filter_by(
                    user_id=current_user.id,
                    company_name=comp.get('name')
                ).first()
                
                if not existing:
                    competitor = Competitor()
                    competitor.user_id = current_user.id
                    competitor.company_name = comp.get('name')
                    competitor.description = comp.get('description')
                    competitor.strengths = comp.get('strengths', [])
                    competitor.weaknesses = comp.get('weaknesses', [])
                    competitor.ad_strategies = comp.get('marketing_strategies', [])
                    db.session.add(competitor)
            
            competitor_insights = competitor_analysis.get('insights', {})
        
        # Step 3: Get industry trends
        flash('Researching industry trends...', 'info')
        if 'get_industry_trends' in globals():
            industry_trends = get_industry_trends(
                current_user.industry or 'general',
                business_data.get('description', '')
            )
        else:
            industry_trends = []
        
        # Step 4: Generate marketing theme
        flash('Creating your marketing theme...', 'info')
        user_document = ""  # Load from user's uploaded document if available
        if 'generate_marketing_theme' in globals():
            marketing_theme = generate_marketing_theme(
                business_data,
                competitor_insights,
                industry_trends,
                user_document
            )
        else:
            marketing_theme = {'theme': 'Default marketing approach'}
        campaign.marketing_theme = json.dumps(marketing_theme)
        
        # Step 5: Generate ad content based on tier
        flash('Generating your creative content...', 'info')
        if 'generate_ad_content' in globals():
            ad_content = generate_ad_content(marketing_theme, business_data)
        else:
            ad_content = {'ad_text': 'Default ad content', 'image_prompt': 'Professional business image'}
        campaign.ad_text = ad_content.get('ad_text', '')
        campaign.image_prompt = ad_content.get('image_prompt', '')
        
        # Step 6: Generate video prompt (Pro tier and above)
        if current_user.can_access_tier(SubscriptionTier.PRO):
            if 'create_veo_prompt' in globals():
                veo_prompt = create_veo_prompt(marketing_theme, business_data, 30)
            else:
                veo_prompt = {'prompt': 'Professional business video', 'duration': 30}
            campaign.video_prompt = veo_prompt
            
            # Step 7: Generate actual video
            flash('Generating your video...', 'info')
            if 'generate_video_with_veo3' in globals():
                video_result = generate_video_with_veo3(
                    prompt=veo_prompt.get('prompt', ''),
                    length_seconds=30,
                    aspect_ratio="9:16"
                )
            else:
                video_result = {'video_path': None, 'success': False}
            # In a real implementation, save the video file path
            # campaign.video_path = video_result.get('video_path')
        
        # Final step: Update campaign status
        campaign.status = 'completed'
        campaign.completed_at = datetime.utcnow()
        db.session.commit()
        
        flash('Campaign generated successfully!', 'success')
        return redirect(url_for('dashboard.view_campaign', campaign_id=campaign.id))
        
    except Exception as e:
        campaign.status = 'failed'
        db.session.commit()
        flash(f'Error processing campaign: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@dashboard.route('/campaign/<campaign_id>')
@login_required
def view_campaign(campaign_id):
    """View completed campaign"""
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Parse marketing theme if it exists
    marketing_theme = {}
    if campaign.marketing_theme:
        try:
            marketing_theme = json.loads(campaign.marketing_theme)
        except:
            pass
    
    return render_template('dashboard/campaign_view.html', 
                         campaign=campaign, 
                         marketing_theme=marketing_theme)

@dashboard.route('/competitors')
@login_required
def competitors():
    """Manage competitors list"""
    if not current_user.can_access_tier(SubscriptionTier.PRO):
        flash('Competitor management requires Pro subscription', 'error')
        return redirect(url_for('auth.pricing'))
    
    user_competitors = Competitor.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/competitors.html', competitors=user_competitors)

@dashboard.route('/competitors', methods=['POST'])
@login_required
def add_competitor():
    """Add custom competitor"""
    if not current_user.can_access_tier(SubscriptionTier.PRO):
        return jsonify({'error': 'Pro subscription required'}), 403
    
    try:
        name = request.form.get('name')
        website = request.form.get('website', '')
        description = request.form.get('description', '')
        
        if not name:
            return jsonify({'error': 'Company name required'}), 400
        
        competitor = Competitor(
            user_id=current_user.id,
            company_name=name,
            website_url=website,
            description=description,
            is_ai_detected=False  # User-added
        )
        db.session.add(competitor)
        db.session.commit()
        
        return jsonify({'success': True, 'id': competitor.id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/competitors/<competitor_id>/delete', methods=['POST'])
@login_required
def delete_competitor(competitor_id):
    """Delete competitor"""
    competitor = Competitor.query.filter_by(id=competitor_id, user_id=current_user.id).first()
    if competitor:
        db.session.delete(competitor)
        db.session.commit()
        flash('Competitor removed', 'success')
    return redirect(url_for('dashboard.competitors'))



@dashboard.route('/download/<campaign_id>/<content_type>')
@login_required
def download_content(campaign_id, content_type):
    """Download generated content"""
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Check tier permissions
    if content_type == 'image' and not current_user.can_access_tier(SubscriptionTier.PLUS):
        flash('Image download requires Plus subscription', 'error')
        return redirect(url_for('auth.pricing'))
    
    if content_type == 'video' and not current_user.can_access_tier(SubscriptionTier.PRO):
        flash('Video download requires Pro subscription', 'error')
        return redirect(url_for('auth.pricing'))
    
    try:
        # Create export using DataExporter
        if DataExporter:
            exporter = DataExporter()
        else:
            flash('Data export service not available', 'error')
            return redirect(url_for('dashboard.profile'))
        campaign_data = {
            'id': campaign.id,
            'title': campaign.title,
            'campaign_goal': campaign.campaign_goal,
            'target_audience': campaign.target_audience,
            'business_url': campaign.business_url,
            'created_at': campaign.created_at.isoformat() if campaign.created_at else '',
            'status': campaign.status,
            'ad_text': campaign.ad_text or '',
            'image_prompt': campaign.image_prompt or '',
            'video_prompt': campaign.video_prompt or ''
        }
        
        if content_type == 'text':
            content = campaign.ad_text or 'No ad content generated'
            filename = f"{campaign.title}_ad_copy.txt"
            response = make_response(content)
            response.headers['Content-Type'] = 'text/plain'
        elif content_type == 'json':
            content = exporter.export_campaign_data(campaign_data, 'json')
            filename = f"{campaign.title}_data.json"
            response = make_response(content)
            response.headers['Content-Type'] = 'application/json'
        elif content_type == 'csv':
            content = exporter.export_campaign_data(campaign_data, 'csv')
            filename = f"{campaign.title}_data.csv"
            response = make_response(content)
            response.headers['Content-Type'] = 'text/csv'
        else:
            flash('Invalid content type', 'error')
            return redirect(url_for('dashboard.campaign_view', campaign_id=campaign_id))
        
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        logging.error(f"Download failed: {e}")
        flash('Download failed - please try again', 'error')
        return redirect(url_for('dashboard.campaign_view', campaign_id=campaign_id))

@dashboard.route('/campaign/<campaign_id>/request-revision', methods=['GET', 'POST'])
@login_required  
def request_revision(campaign_id):
    """Handle user revision requests"""
    campaign = Campaign.query.filter_by(id=campaign_id, user_id=current_user.id).first()
    if not campaign:
        flash('Campaign not found', 'error')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        # Validate revision request
        if FormValidator:
            form_data = FormValidator.sanitize_form_data(dict(request.form))
            is_valid, errors = FormValidator.validate_revision_form(form_data)
        else:
            form_data = dict(request.form)
            is_valid = True
            errors = []
        
        if not is_valid:
            for field, field_errors in errors.items():
                for error in field_errors:
                    flash(error, 'error')
            return render_template('dashboard/request_revision.html', campaign=campaign)
        
        try:
            # Create revision record (would need to add CampaignRevision model)
            revision_type = form_data.get('revision_type', 'text')
            user_notes = form_data.get('user_notes', '')
            
            # Initialize AI processor for revision
            if not AIProcessor:
                flash('AI revision service not available', 'error')
                return render_template('dashboard/request_revision.html', campaign=campaign)
            ai_processor = AIProcessor()
            business_info = json.loads(campaign.business_metadata) if campaign.business_metadata else {}
            
            # Process revision based on type
            if revision_type == 'text' and campaign.ad_text:
                revised_content = ai_processor.process_user_revision(
                    campaign.ad_text, user_notes, business_info, 'text'
                )
                campaign.ad_text = revised_content
                
            elif revision_type == 'image' and campaign.image_prompt:
                revised_prompt = ai_processor.process_user_revision(
                    campaign.image_prompt, user_notes, business_info, 'image'
                )
                campaign.image_prompt = revised_prompt
                
            elif revision_type == 'all':
                # Regenerate entire campaign with feedback
                content_data = ai_processor.generate_marketing_campaign(
                    business_info, 
                    campaign.campaign_goal,
                    f"{campaign.target_audience}. User feedback: {user_notes}",
                    current_user.subscription_tier.value
                )
                
                campaign.ad_text = content_data.get('ad_text', campaign.ad_text)
                if current_user.can_access_tier('plus'):
                    campaign.image_prompt = content_data.get('image_prompt', campaign.image_prompt)
                if current_user.can_access_tier('pro'):
                    campaign.video_prompt = json.dumps(content_data.get('video_prompt', {}))
            
            db.session.commit()
            flash('Your content has been revised based on your feedback!', 'success')
            return redirect(url_for('dashboard.campaign_view', campaign_id=campaign_id))
            
        except Exception as e:
            logging.error(f"Revision failed: {e}")
            flash('Revision processing failed - please try again', 'error')
    
    return render_template('dashboard/request_revision.html', campaign=campaign)

@dashboard.route('/export-data')
@login_required
def export_dashboard():
    """Data export dashboard"""
    campaigns = Campaign.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/export_data.html', campaigns=campaigns)

@dashboard.route('/download-app')
@login_required
def download_app():
    """Download the entire app as a zip file"""
    import zipfile
    import tempfile
    import os
    from flask import send_file
    
    # Create a temporary zip file
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, 'dominate_marketing_app.zip')
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the project directory
            for root, dirs, files in os.walk('.'):
                # Skip certain directories
                if any(skip in root for skip in ['.git', '__pycache__', 'node_modules', '.env', 'venv']):
                    continue
                    
                for file in files:
                    # Skip certain file types
                    if file.endswith(('.pyc', '.pyo', '.log', '.db')):
                        continue
                        
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arcname)
        
        return send_file(zip_path, as_attachment=True, download_name='dominate_marketing_app.zip')
        
    except Exception as e:
        logging.error(f"App download failed: {e}")
        flash('Download failed - please try again', 'error')
        return redirect(url_for('dashboard.index'))

@dashboard.route('/export-bulk/<export_format>')
@login_required
def export_bulk_data(export_format):
    """Export all user campaigns in specified format"""
    try:
        campaigns = Campaign.query.filter_by(user_id=current_user.id).all()
        if not DataExporter:
            flash('Data export service not available', 'error')
            return redirect(url_for('dashboard.export_dashboard'))
        exporter = DataExporter()
        
        if export_format not in ['json', 'csv']:
            flash('Invalid export format', 'error')
            return redirect(url_for('dashboard.export_dashboard'))
        
        # Prepare bulk data
        bulk_data = []
        for campaign in campaigns:
            campaign_data = {
                'id': campaign.id,
                'title': campaign.title,
                'campaign_goal': campaign.campaign_goal,
                'target_audience': campaign.target_audience,
                'business_url': campaign.business_url,
                'created_at': campaign.created_at.isoformat() if campaign.created_at else '',
                'status': campaign.status,
                'ad_text': campaign.ad_text or '',
                'image_prompt': campaign.image_prompt or '',
                'video_prompt': campaign.video_prompt or ''
            }
            bulk_data.append(campaign_data)
        
        if export_format == 'json':
            content = json.dumps(bulk_data, indent=2)
            content_type = 'application/json'
            filename = f"dominate_marketing_campaigns_{datetime.now().strftime('%Y%m%d')}.json"
        else:  # CSV
            # Create CSV with all campaigns
            lines = ["Campaign ID,Title,Goal,Target Audience,Business URL,Created,Status,Ad Text Length"]
            for data in bulk_data:
                ad_length = len(data.get('ad_text', ''))
                lines.append(f"\"{data['id']}\",\"{data['title']}\",\"{data['campaign_goal']}\",\"{data['target_audience']}\",\"{data['business_url']}\",\"{data['created_at']}\",\"{data['status']}\",{ad_length}")
            
            content = '\n'.join(lines)
            content_type = 'text/csv'
            filename = f"dominate_marketing_campaigns_{datetime.now().strftime('%Y%m%d')}.csv"
        
        response = make_response(content)
        response.headers['Content-Type'] = content_type
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        logging.error(f"Bulk export failed: {e}")
        flash('Export failed - please try again', 'error')
        return redirect(url_for('dashboard.export_dashboard'))

@dashboard.route('/analytics')
@login_required
def analytics():
    """Marketing analytics dashboard"""
    campaigns = Campaign.query.filter_by(user_id=current_user.id).all()
    
    # Calculate analytics
    total_campaigns = len(campaigns)
    completed_campaigns = len([c for c in campaigns if c.status == 'completed'])
    processing_campaigns = len([c for c in campaigns if c.status == 'processing'])
    
    # Campaign goals breakdown
    goals_breakdown = {}
    for campaign in campaigns:
        goal = campaign.campaign_goal or 'unknown'
        goals_breakdown[goal] = goals_breakdown.get(goal, 0) + 1
    
    # Industry statistics (mock data for demonstration)
    industry_stats = {
        'avg_agency_cost_monthly': 8500,
        'avg_agency_time_weeks': 3,
        'dominate_cost_monthly': current_user.subscription_tier.value == 'enterprise' and 299 or 99,
        'dominate_time_minutes': 5,
        'trend_data_age_hours': 6,
        'traditional_data_age_years': 20,
        'update_frequency_minutes': 20
    }
    
    return render_template('dashboard/analytics.html', 
                         campaigns=campaigns,
                         total_campaigns=total_campaigns,
                         completed_campaigns=completed_campaigns,
                         processing_campaigns=processing_campaigns,
                         goals_breakdown=goals_breakdown,
                         industry_stats=industry_stats)

# Brand Management Routes
@dashboard.route('/brands')
@login_required
def brands():
    """Display user's brands"""
    brands = Brand.query.filter_by(user_id=current_user.id).order_by(Brand.created_at.desc()).all()
    return render_template('dashboard/brands.html', brands=brands)

@dashboard.route('/add-brand')
@login_required
def add_brand():
    """Add new brand form"""
    return render_template('dashboard/add_brand.html')

@dashboard.route('/add-brand', methods=['POST'])
@login_required
def add_brand_post():
    """Process new brand creation"""
    try:
        # Extract and validate form data
        name = request.form.get('name', '').strip()
        website_url = request.form.get('website_url', '').strip()
        industry = request.form.get('industry', '').strip()
        description = request.form.get('description', '').strip()
        logo_url = request.form.get('logo_url', '').strip()
        subscription_tier = request.form.get('subscription_tier', 'basic')
        
        if not name:
            flash('Brand name is required', 'error')
            return redirect(url_for('dashboard.add_brand'))
        
        # Create new brand
        new_brand = Brand()
        new_brand.user_id = current_user.id
        new_brand.name = name
        new_brand.website_url = website_url if website_url else None
        new_brand.industry = industry if industry else None
        new_brand.description = description if description else None
        new_brand.logo_url = logo_url if logo_url else None
        new_brand.subscription_tier = SubscriptionTier(subscription_tier)
        
        db.session.add(new_brand)
        db.session.commit()
        
        flash(f'Brand "{name}" created successfully! Set up billing to activate.', 'success')
        return redirect(url_for('dashboard.view_brand', brand_id=new_brand.id))
        
    except Exception as e:
        logging.error(f"Error creating brand: {str(e)}")
        flash('Error creating brand. Please try again.', 'error')
        return redirect(url_for('dashboard.add_brand'))

@dashboard.route('/brand/<brand_id>')
@login_required
def view_brand(brand_id):
    """View brand details and campaigns"""
    brand = Brand.query.filter_by(id=brand_id, user_id=current_user.id).first()
    if not brand:
        flash('Brand not found', 'error')
        return redirect(url_for('dashboard.brands'))
    
    # Get campaigns for this brand
    campaigns = Campaign.query.filter_by(brand_id=brand_id, user_id=current_user.id).order_by(Campaign.created_at.desc()).all()
    
    return render_template('dashboard/view_brand.html', brand=brand, campaigns=campaigns)

@dashboard.route('/brand/<brand_id>/edit')
@login_required
def edit_brand(brand_id):
    """Edit brand form"""
    brand = Brand.query.filter_by(id=brand_id, user_id=current_user.id).first()
    if not brand:
        flash('Brand not found', 'error')
        return redirect(url_for('dashboard.brands'))
    
    return render_template('dashboard/edit_brand.html', brand=brand)
# Social Media Authentication Routes
@dashboard.route('/auth/social/<platform>')
@login_required
def social_auth(platform):
    """Initiate social media OAuth flow"""
    from services.social_auth_service import social_auth_service
    
    try:
        redirect_uri = url_for('dashboard.social_callback', platform=platform, _external=True)
        auth_url = social_auth_service.get_auth_url(platform, str(current_user.id), redirect_uri)
        
        if not auth_url:
            flash(f'{platform.title()} authentication is not configured', 'error')
            return redirect(url_for('dashboard.social_scheduling'))
        
        return redirect(auth_url)
        
    except Exception as e:
        flash(f'Error initiating {platform} authentication: {str(e)}', 'error')
        return redirect(url_for('dashboard.social_scheduling'))

@dashboard.route('/auth/social/<platform>/callback')
@login_required
def social_callback(platform):
    """Handle social media OAuth callback"""
    from services.social_auth_service import social_auth_service
    
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            flash(f'{platform.title()} authentication failed: {error}', 'error')
            return redirect(url_for('dashboard.social_scheduling'))
        
        if not code:
            flash(f'No authorization code received from {platform.title()}', 'error')
            return redirect(url_for('dashboard.social_scheduling'))
        
        redirect_uri = url_for('dashboard.social_callback', platform=platform, _external=True)
        result = social_auth_service.handle_oauth_callback(platform, code, state or "", redirect_uri)
        
        if result['success']:
            flash(f'{platform.title()} account connected successfully!', 'success')
        else:
            flash(f'Failed to connect {platform.title()}: {result.get("error")}', 'error')
        
        return redirect(url_for('dashboard.social_scheduling'))
        
    except Exception as e:
        flash(f'Error connecting {platform} account: {str(e)}', 'error')
        return redirect(url_for('dashboard.social_scheduling'))
