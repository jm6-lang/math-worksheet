<?php
/*
 * @Author        : Qinver
 * @Url           : zibll.com
 * @Date          : 2020-09-29 13:18:36
 * @LastEditTime: 2022-12-08 22:11:40
 * @Email         : 770349780@qq.com
 * @Project       : Zibll子比主题
 * @Read me       : 感谢您使用子比主题，主题源码有详细的注释，支持二次开发。
 * @Remind        : 使用盗版主题会存在各种未知风险。支持正版，从我做起！
 */

?>
<!DOCTYPE HTML>
<html <?php echo 'lang="' . esc_attr(get_bloginfo('language')) . '"'; ?>>
<head>
	<meta charset="UTF-8">
	<link rel="dns-prefetch" href="//apps.bdimg.com">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=0.0, viewport-fit=cover">
	<meta http-equiv="Cache-Control" content="no-transform" />
	<meta http-equiv="Cache-Control" content="no-siteapp" />
	<meta name="baidu-site-verification" content="codeva-QN1Xz77WWE" />
	<meta name="msvalidate.01" content="04F419B0639E60348D95F499D9274280" />
	<meta name="baidu-site-verification" content="codeva-OmiwxxIsnF" />
	<meta property="bytedance:published_time" content="2014-12-11T12:28:44+01:00" />
	<meta property="bytedance:lrDate_time" content="2017-03-13T15:01:40+01:00" />
	<meta property="bytedance:updated_time" content="2017-03-13T15:01:40+01:00" />
	<?php wp_head();?>
	<?php tb_xzh_head_var();?>
	<script>
(function(){
var el = document.createElement("script");
el.src = "https://lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?10ed676cc2eedcf0ce1054871716a2bb1879abd64896b1cac5172297c2413f9ebc434964556b7d7129e9b750ed197d397efd7b0c6c715c1701396e1af40cec962b8d7c8c6655c9b00211740aa8a98e2e";
el.id = "ttzz";
var s = document.getElementsByTagName("script")[0];
s.parentNode.insertBefore(el, s);
})(window)
</script>
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?ae9db5ace03b20e6544a73680ef84a3a";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
</head>
<body <?php body_class(_bodyclass());?>>
	<?php echo qj_dh_nr(); ?>
	<?php zib_seo_image();?>
	<?php zib_header();?>
	<!--调用信息代码-->
<!--底部统计用的代码-->
<script type="text/javascript" >
<?php
//用户总数
$users = $wpdb->get_var("SELECT COUNT(ID) FROM $wpdb->users");echo "var tj_jstext="."'$users'";
?>
</script>
<script type="text/javascript" >
<?php
/*
 * WordPress获取今日发布文章数量
 */
function nd_get_24h_post_count(){
  $today = getdate();
  $query = new WP_Query( 'year=' . $today["year"] . '&monthnum=' . $today["mon"] . '&day=' . $today["mday"]);
  $postsNumber = $query->found_posts;
  return $postsNumber;
}
$post_24h = nd_get_24h_post_count();
echo "var tj_24h="."'$post_24h'";
?>
</script>
<script type="text/javascript" >
<?php
/*
 * WordPress整站文章访问计数
 */
function nd_get_all_view(){
  global $wpdb;
  $count=0;
  $views= $wpdb->get_results("SELECT * FROM $wpdb->postmeta WHERE meta_key='views'");
  foreach($views as $key=>$value){
    $meta_value=$value->meta_value;
    if($meta_value!=' '){
      $count+=(int)$meta_value;
    }
  }return $count;
}
$post_view = nd_get_all_view();
echo "var tj_view="."'$post_view'";
?>
</script>
<script type="text/javascript" >
<?php
//日志总数
$count_posts = wp_count_posts(); 
$published_posts =$count_posts->publish;
echo "var tj_rzzs="."'$published_posts'";
?>
</script>
<script type="text/javascript" >
<?php
//稳定运行
$wdyx_time = floor((time()-strtotime("2023-3-12"))/86400);
echo "var tj_wdyx="."'$wdyx_time'";
?>
</script>
<!--调用信息代码结束-->