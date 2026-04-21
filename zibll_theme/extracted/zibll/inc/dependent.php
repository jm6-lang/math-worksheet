<?php
/*
 * @Author        : Qinver
 * @Url           : zibll.com
 * @Date          : 2020-12-23 22:31:32
 * @LastEditTime: 2024-06-12 23:16:38
 * @Email         : 770349780@qq.com
 * @Project       : Zibll子比主题
 * @Description   : 一款极其优雅的Wordpress主题|前置依赖函数
 * @Read me       : 感谢您使用子比主题，主题源码有详细的注释，支持二次开发。
 * @Remind        : 使用盗版主题会存在各种未知风险。支持正版，从我做起！
 */

/**
 * @description: 根据页面模板获取页面链接
 * @param {*} $template
 * @return {*}
 */
function zib_get_template_page_url($template, $args = array())
{
    $cache = wp_cache_get($template, 'page_url', true);
    if ($cache !== false) {
        return $cache;
    }

    $templates = array(
        'pages/newposts.php'  => array('发布文章', 'newposts'),
        'pages/user-sign.php' => array('登录/注册/找回密码', 'user-sign'),
        'pages/download.php'  => array('资源下载', 'download'),
    );
    $templates = array_merge($templates, $args);

    //查找是否已经存在
    $query_args = array(
        'orderby'                => 'date',
        'order'                  => 'ASC',
        'update_post_term_cache' => false,
        'update_post_meta_cache' => false,
        'showposts'              => 1,
        'ignore_sticky_posts'    => true,
        'no_found_rows'          => true,
        'post_type'              => 'page',
        'post_status'            => 'publish',
        'fields'                 => 'ids',
        'meta_query'             => array(
            array(
                'key'   => '_wp_page_template',
                'value' => $template,
            )),
    );
    $query = new WP_Query($query_args);
    $pages = $query->get_posts();

    $page_id = 0;
    if (!empty($pages[0])) {
        $page_id = $pages[0];
    } elseif (!empty($templates[$template][0])) {
        $one_page = array(
            'post_title'  => $templates[$template][0],
            'post_name'   => $templates[$template][1],
            'post_status' => 'publish',
            'post_type'   => 'page',
            'post_author' => 1,
        );

        $page_id = wp_insert_post($one_page);
        update_post_meta($page_id, '_wp_page_template', $template);
    }
    if ($page_id) {
        $url = get_permalink($page_id);
        wp_cache_set($template, $url, 'page_url');
        return $url;
    } else {
        return false;
    }
}

//获取经验值add的参数
function zib_get_user_integral_add_options()
{
    $options = array(
        'sign_up'         => array('首次注册', 20, '', '用户'),
        'sign_in'         => array('每日登录', 5, '每日登录', '用户'),
        'followed'        => array('被关注', 5, '有新的粉丝关注', '用户'),

        'post_new'        => array('发布文章', 5, '发布优质文章并审核通过', '文章'),
        'post_like'       => array('文章获赞', 1, '发布内容获得用户点赞，每篇文章最多加5次', '文章'),
        'post_favorite'   => array('文章被收藏', 2, '发布的内容被用户收藏', '文章'),
        'comment_new'     => array('发表评论', 2, '发表评论并审核通过', '文章'),
        'comment_like'    => array('评论获赞', 1, '发布评论获得用户点赞，每个评论最多加5次', '文章'),

        'bbs_posts_new'   => array('发布帖子', 3, '发布优质帖子并审核通过', '论坛'),
        'bbs_score_extra' => array('帖子被加分', 1, '帖子被加分，每篇帖子最多加5次', '论坛'),
        'bbs_essence'     => array('帖子评为精华', 2, '帖子评为精华', '论坛'),
        'bbs_posts_hot'   => array('帖子成为热门', 2, '帖子成为热门', '论坛'),
        'bbs_plate_new'   => array('创建版块', 2, '创建新版块并审核通过', '论坛'),
        'bbs_plate_hot'   => array('版块成为热门', 2, '创建的版块成为热门版块', '论坛'),
        'bbs_adopt'       => array('回答被采纳', 2, '回答被提问作者采纳', '论坛'),
        'bbs_comment_hot' => array('评论成为神评', 2, '发表的评论成为神评论', '论坛'),
    );
    return apply_filters('integral_add_options', $options);
}

// 获取及设置主题配置参数
function _pz($name, $default = false, $subname = '')
{
    //声明静态变量，加速获取
    static $options = null;
    if ($options === null) {
        $options = get_option('zibll_options');
    }

    if (isset($options[$name])) {
        if ($subname) {
            return isset($options[$name][$subname]) ? $options[$name][$subname] : $default;
        } else {
            return $options[$name];
        }
    }
    return $default;
}

function _spz($name, $value)
{
    $get_option        = get_option('zibll_options');
    $get_option        = is_array($get_option) ? $get_option : array();
    $get_option[$name] = $value;
    return update_option('zibll_options', $get_option);
}

//获取一个随机数
function zib_get_mt_rand_number($var)
{
    $defaults = array(
        'max' => 0,
        'min' => 0,
    );
    $var = wp_parse_args((array) $var, $defaults);

    return @mt_rand((int) $var['min'], (int) $var['max']);
}

function zib_get_csf_option_new_badge()
{
    return array(
        '7.0' => '<badge style="background: #ff876b;">V7.0</badge>',
        '7.1' => '<badge style="background: #ff876b;">V7.1</badge>',
        '7.2' => '<badge style="background: #ff876b;">V7.2</badge>',
        '7.3' => '<badge style="background: #ff876b;">V7.3</badge>',
        '7.4' => '<badge>NEW</badge>',
        '7.5' => '<badge>NEW</badge>',
        '7.6' => '<badge>NEW</badge>',
        '7.7' => '<badge>NEW</badge>',
        '7.8' => '<badge>NEW</badge>',
    );
}
