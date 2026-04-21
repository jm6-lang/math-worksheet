import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# New home-1.php - only mobile ad slots
new_home = '''<?php
/* Template Name: Home-1 */
if(!defined('ABSPATH')) exit;
add_filter('body_class', function($classes) { return array_merge($classes, array('home')); });
get_header(); ?>
<style>
/* News ticker - desktop */
.news-ticker-box { height: 120px; display: flex; align-items: stretch; overflow: hidden; background: #fff; border-radius: 8px; border: 1px solid #eee; }
.ticker-label { width: 100px; background: #FF5E52; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
.ticker-wrapper { flex: 1; height: 120px; overflow: hidden; position: relative; padding: 0 15px; }
.ticker-list { list-style: none; padding: 0; margin: 0; transition: transform 0.5s ease-in-out; }
.ticker-list li { height: 40px; line-height: 40px; border-bottom: 1px solid #f9f9f9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ticker-list li:last-child { border-bottom: none; }
.ticker-list li a { color: #333; text-decoration: none; font-size: 14px; }
.ticker-list li a:hover { color: #FF5E52; }
.ticker-time { color: #999; margin-right: 10px; font-family: monospace; }

/* Mobile ticker - smaller */
@media screen and (max-width: 768px) {
    .news-ticker-box { height: 80px; border-radius: 6px; }
    .ticker-label { width: 70px; font-size: 12px; }
    .ticker-wrapper { height: 80px; padding: 0 10px; }
    .ticker-list li { height: 26px; line-height: 26px; font-size: 12px; }
    .ticker-list li a { font-size: 12px; }
}
@media screen and (max-width: 400px) {
    .news-ticker-box { height: 60px; }
    .ticker-label { width: 55px; font-size: 11px; }
    .ticker-wrapper { height: 60px; padding: 0 8px; }
    .ticker-list li { height: 20px; line-height: 20px; font-size: 11px; }
    .ticker-list li a { font-size: 11px; }
    .ticker-time { font-size: 10px; }
}

/* Ad slots - mobile only */
.ad-slot-mobile { display: none; background: #f8f9fa; border: 1px dashed #ddd; border-radius: 8px; align-items: center; justify-content: center; min-height: 60px; margin: 12px 0; }
.ad-slot-label { color: #999; font-size: 11px; }
@media screen and (max-width: 768px) {
    .ad-slot-mobile { display: flex; }
}
</style>

<div class="yy-main">
    <!-- Ad Slot 1: After Header (Mobile Only) -->
    <div class="container ad-slot-mobile" style="margin-top: 10px;">
        <span class="ad-slot-label">广告位 1</span>
    </div>

    <div class="yy-group slider-section">
        <div class="container">
            <?php 
            $slides = [
                ['src'=>'https://sc01.alicdn.com/kf/A5c6bc13e6ae642388d5e84a00b091e57H.jpg','title'=>'互联网项目教程','desc'=>'365天不间断更新全网最火创业资源','url'=>'#']
            ];
            ?>
            <div id="homeSlider" class="carousel slide rounded-lg overflow-hidden shadow-lg" data-ride="carousel">
                <div class="carousel-inner">
                    <?php foreach($slides as $i => $slide): ?>
                    <div class="carousel-item active">
                        <a href="<?php echo $slide['url']?:'#'; ?>">
                            <img src="<?php echo $slide['src']; ?>" class="d-block w-100" style="object-fit: contain; background: #000; height: 450px; max-height: 60vh;">
                            <div class="carousel-caption" style="text-align: right; left: auto; right: 30px; bottom: 30px; background: rgba(0,0,0,0.6); padding: 20px 30px; border-radius: 15px; backdrop-filter: blur(5px); max-width: 400px; width: auto;">
                                <h2 style="font-weight: 800; font-size: 1.8rem; margin-bottom: 5px; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);"><?php echo $slide['title']; ?></h2>
                                <p style="font-size: 1rem; opacity: 0.9; margin: 0; color: #eee;"><?php echo $slide['desc']; ?></p>
                            </div>
                        </a>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Orange Notice Section -->
    <div class="orange-notice-bar" style="margin-top:15px;">
        <div class="container">
            <div style="background:#ff9800; color:#fff; padding:12px 20px; border-radius:8px; display:flex; align-items:center; gap:15px; box-shadow:0 4px 12px rgba(255,152,0,0.2);">
                <i class="fas fa-exclamation-circle" style="font-size:18px;"></i>
                <div style="font-size:14px; font-weight:600; flex:1;">网站公告：欢迎来到互联网项目教程，本站每日实时更新全网最火爆的副业赚钱项目，助您快速掌握一线资讯！</div>
                <a href="/copyright" style="color:#fff; text-decoration:underline; font-size:12px; opacity:0.9;">查看版权协议</a>
            </div>
        </div>
    </div>

    <!-- News Ticker Section -->
    <div class="news-ticker-section">
        <div class="container">
            <div class="news-ticker-box">
                <div class="ticker-label"><i class="fa fa-bullhorn"></i> 最新动态</div>
                <div class="ticker-wrapper">
                    <ul class="ticker-list">
                        <?php
                        $latest_news = new WP_Query(array(
                            'post_type' => array('post', 'product'),
                            'posts_per_page' => 10,
                            'orderby' => 'date',
                            'order' => 'DESC'
                        ));
                        if($latest_news->have_posts()): while($latest_news->have_posts()): $latest_news->the_post(); ?>
                            <li><a href="<?php the_permalink(); ?>"><span class="ticker-time">[<?php echo get_the_date('m-d'); ?>]</span> <?php the_title(); ?></a></li>
                        <?php endwhile; wp_reset_postdata(); endif; ?>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Ad Slot 2: After News Ticker (Mobile Only) -->
    <div class="container ad-slot-mobile" style="min-height: 50px;">
        <span class="ad-slot-label">广告位 2</span>
    </div>

    <!-- Global Search Section -->
    <div class="search-section my-4">
        <div class="container">
            <form role="search" method="get" class="search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
                <div class="search-input-group">
                    <div class="input-wrapper">
                        <i class="fa fa-search search-icon"></i>
                        <input type="search" class="search-field" placeholder="搜索全站海量资源..." value="<?php echo get_search_query(); ?>" name="s" required />
                    </div>
                    <button type="submit" class="search-submit">搜索</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Ad Slot 3: Before Content (Mobile Only) -->
    <div class="container ad-slot-mobile" style="min-height: 50px;">
        <span class="ad-slot-label">广告位 3</span>
    </div>

    <div class="yy-group">
        <div class="container">
            <div class="section-header text-center mb-5">
                <h3><?php echo yy_get('last_published_alias') ?: '最新发布的资源'; ?></h3>
                <div class="desc"><?php echo yy_get('last_published_description') ?: '为您精选最新的干货资源，每日更新不间断。'; ?></div>
            </div>
            <div class="product-list">
                <?php
                if ( get_query_var('paged') ) { $paged = get_query_var('paged'); } elseif ( get_query_var('page') ) { $paged = get_query_var('page'); } else { $paged = 1; } 
                $query = new WP_Query(['post_type'=>['post','product'],'orderby'=>'date','posts_per_page'=>yy_get('resource_quantity')?:12,'paged'=>$paged]);
                if($query->have_posts()): while($query->have_posts()): $query->the_post(); ?>
                <div class="card">
                    <div class="card-body">
                        <a class="thumbnail" href="<?php the_permalink()?>">
                            <img src="<?php echo yy_get_thumb(); ?>" alt="<?php the_title() ?>" />
                        </a>
                        <div class="data">
                            <h4 class="card-title"><a href="<?php the_permalink()?>"><?php the_title() ?></a></h4>
                            <div class="bottom-data">
                                <span class="time"><?php echo get_the_date('Y-m-d'); ?></span>
                                <span class="price"><?php echo xc_get_price(get_the_ID()) ?: ''; ?></span>
                            </div>
                        </div>
                    </div>
                </div>
                <?php endwhile; wp_reset_postdata(); endif; ?>
            </div>
            <ul class="pagination">
                <?php echo paginate_links(['total'=>$query->max_num_pages, 'current'=>$paged, 'format'=>'page/%#%/']); ?>
            </ul>
        </div>
    </div>

    <!-- Ad Slot 4: After Content (Mobile Only) -->
    <div class="container ad-slot-mobile" style="min-height: 50px; margin-bottom: 15px;">
        <span class="ad-slot-label">广告位 4</span>
    </div>
</div>

<script>
jQuery(document).ready(function($) {
    var ticker = $('.ticker-list');
    var items = ticker.find('li');
    if (items.length <= 1) return;
    
    var itemHeight = 40; 
    var currentIndex = 0;

    function scrollTicker() {
        currentIndex += 1;
        
        if (currentIndex >= items.length) {
            ticker.css('transition', 'none');
            ticker.css('transform', 'translateY(0)');
            currentIndex = 0;
            ticker[0].offsetHeight;
            ticker.css('transition', 'transform 0.5s ease-in-out');
        } else {
            ticker.css('transform', 'translateY(-' + (currentIndex * itemHeight) + 'px)');
        }
    }
    setInterval(scrollTicker, 3000); 
});
</script>

<?php get_footer(); ?>
'''

# Write
cmd = f"cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php << 'PHPEOF'\n{new_home}\nPHPEOF"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
err = stderr.read().decode('utf-8', errors='replace')
if err:
    print(f'ERROR: {err[:500]}')
else:
    # Verify
    stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" https://www.skillxm.cn/', timeout=15)
    code = stdout.read().decode().strip()
    print(f'OK - 桌面端广告位已移除，仅保留移动端 4 个广告位')
    print(f'Site HTTP: {code}')

ssh.close()
