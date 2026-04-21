<?php

/**
 * Functions
 *
 * @package YYMarket
 */

require __DIR__ . '/vessel/vessel.php';
require __DIR__ . '/xenice/functions.php';

/**
 * Get option
 */
function yy_get( $name) {
    return vessel\get($name);
}

/**
 * Get page
 */
function yy_get_page($template)
{
    global $wpdb;
    $page_id = $wpdb->get_var($wpdb->prepare("SELECT `post_id` 
    FROM `$wpdb->postmeta`, `$wpdb->posts`
    WHERE `post_id` = `ID`
    AND `post_status` = 'publish'
    AND `meta_key` = '_wp_page_template'
    AND `meta_value` = %s
    LIMIT 1;", $template));
    if($page_id){
        return get_post($page_id);
    }
}

/**
 * Import template
 */
function yy_import($name){
    $file = apply_filters('yy_import_file', '', $name);
    if(is_file($file)){
        include($file);
        return true;
    }
}

/**
 * Breadcrumb
 */
function yy_breadcrumb() {
	function yy_get_greadcrumb( $cid, $taxonomy ) {
		if ( is_date() ) {
			echo '<span class="breadcrumb-item active">' . esc_html( get_the_date('Y-m-d') ) . '</span>';
			return;
		}
		$row = get_term( $cid, $taxonomy );
		$pid = $row->parent;
		if ( $pid ) {
			yy_get_greadcrumb( $pid, $taxonomy);
		}
		echo '<a class="breadcrumb-item" href="' . esc_attr( get_term_link( $row->term_id, $taxonomy ) ) . '">' . esc_html( $row->name ) . '</a>';
	}

	if ( is_single() ) {
		global $post;
		global $wpdb;
		$cats = wp_get_post_categories( $post->ID );
		echo '<a class="breadcrumb-item" href="' . esc_attr( home_url() ) . '">' . esc_html__( 'Home', 'onenice' ) . '</a>';
		$cid = $cats[0]??0;
		if ( $cid ) {
			$taxonomy = wp_cache_get( 'taxonomy_' . $cid, 'yy_cache_group' );
			if ( false === $taxonomy ) {
				$taxonomy = $wpdb->get_var( $wpdb->prepare( "SELECT taxonomy FROM {$wpdb->term_taxonomy} WHERE term_id=%d", $cid ) );
				wp_cache_set( 'taxonomy_' . $cid, $taxonomy, 'yy_cache_group' );
			}
			yy_get_greadcrumb( $cid, $taxonomy );
		}
		echo '<span class="breadcrumb-item active">' . esc_html( $post->post_title ) . '</span>';
	} elseif ( is_archive() ) {
		global $wpdb;
		$cid      = get_queried_object_id();
		$taxonomy = wp_cache_get( 'taxonomy_' . $cid, 'yy_cache_group' );
		if ( false === $taxonomy ) {
			$taxonomy = $wpdb->get_var( $wpdb->prepare( "SELECT taxonomy FROM {$wpdb->term_taxonomy} WHERE term_id=%d", $cid ) );
			wp_cache_set( 'taxonomy_' . $cid, $taxonomy, 'yy_cache_group' );
		}
		echo '<a class="breadcrumb-item" href="' . esc_attr( home_url() ) . '">' . esc_html__( 'Home', 'onenice' ) . '</a>';
		yy_get_greadcrumb( $cid, $taxonomy );
	}
}

/**
 * Thumbnail logic
 */
function yy_get_thumb($post_id = null, $size = 'full') {
    if (!$post_id) {
        $post_id = get_the_ID();
    }
    if (!$post_id) return '';
    $thumbnail_id = get_post_thumbnail_id($post_id);
    $thumbnail_url = wp_get_attachment_image_url($thumbnail_id, $size);
    if(!$thumbnail_url){
        $thumbnail_url = get_post_meta($post_id, 'fifu_image_url', true);
    }
    if(!$thumbnail_url){
        $thumbnail_url = 'https://images.unsplash.com/photo-1557683316-973673baf926?q=50&w=400';
    }
    return $thumbnail_url;
}

if ( function_exists( 'add_theme_support' ) ) {
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'automatic-feed-links' );
}
register_nav_menus( array( 'main-menu' => __( 'Main Menu', 'onenice' ) ) );

add_action( 'widgets_init', function() {
	register_sidebar(array('id'=>'home','name'=>__('Home','onenice'),'before_title'=>'<h3>','after_title'=>'</h3>'));
	register_sidebar(array('id'=>'single','name'=>__('Posts','onenice'),'before_title'=>'<h3>','after_title'=>'</h3>'));
	register_sidebar(array('id'=>'archive','name'=>__('archive','onenice'),'before_title'=>'<h3>','after_title'=>'</h3>'));
});

add_action( 'pre_get_posts', function($query) {
	if ( $query->is_home() && $query->is_main_query() ) {
		$query->set( 'ignore_sticky_posts', 1 );
	}
});

add_filter( 'the_excerpt', function($excerpt) {
	$excerpt = wp_strip_all_tags( $excerpt );
	$max_len = intval(yy_get( 'excerpt_length' ));
	if(mb_strlen($excerpt)>$max_len && $max_len > 0){
        return mb_substr($excerpt, 0, (int)$max_len).'...';
    }
    return $excerpt;
});

add_filter( 'post_thumbnail_url', function($url) {
	return $url ?: yy_get( 'site_thumbnail' );
}, 999);

add_action( 'wp_enqueue_scripts', function() {
    $cdn_url = 'https://cdn.bootcdn.net/ajax/libs';
    wp_enqueue_style( 'font-awesome', $cdn_url . '/font-awesome/4.7.0/css/font-awesome.min.css' );
    wp_enqueue_style( 'bootstrap', $cdn_url . '/twitter-bootstrap/4.4.1/css/bootstrap.min.css' );
    wp_enqueue_script( 'bootstrap', $cdn_url . '/twitter-bootstrap/4.4.1/js/bootstrap.min.js', array('jquery'), '4.4.1', true );
    wp_enqueue_style( 'yymarket', STATIC_URL . '/css/style.css' );
    wp_enqueue_style( 'yymarket-custom', STATIC_URL . '/css/custom.css', array('yymarket') );
    wp_enqueue_script( 'yymarket', STATIC_URL . '/js/script.js', array('jquery'), '1.0', true );
});

add_action( 'wp_head', function() {
    echo '<style>:root{--yy-main-color:#FF5E52;}</style>';
});

/**
 * Force SMTP settings
 */
add_action('phpmailer_init', function($phpmailer){
    $phpmailer->isSMTP();
    $phpmailer->Host = 'smtp.qq.com';
    $phpmailer->SMTPAuth = true;
    $phpmailer->Port = 465;
    $phpmailer->SMTPSecure = 'ssl';
    $phpmailer->Username = '644428571@qq.com';
    $phpmailer->Password = 'ghxfcuyubrjcbeec';
    $phpmailer->From = '644428571@qq.com';
    $phpmailer->FromName = '小二郎资源网';
}, 999);

/**
 * Completely disable comments
 */
add_filter('comments_open', '__return_false', 20, 2);
add_filter('pings_open', '__return_false', 20, 2);
add_filter('comments_array', '__return_empty_array', 10, 2);
