import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

wp_config = """<?php
/**
 * The base configuration for WordPress
 */
define( 'DB_NAME', 'wp_skillxm' );
define( 'DB_USER', 'wpuser' );
define( 'DB_PASSWORD', 'WpPass2024!' );
define( 'DB_HOST', 'localhost' );
define( 'DB_CHARSET', 'utf8mb4' );
define( 'DB_COLLATE', '' );

define( 'AUTH_KEY', 'gIP$Y}XN0MC+]sT=@T2g+tf~8b>mzRTBul3L/.S.%|VCMr]sk`]@GDr<]34t?g5K' );
define( 'SECURE_AUTH_KEY', '9j^&Y;sli@^iJ^a=wt5 #)4;<Xt&hrM3GrGvYK$5`EmW}@HX2{AfaCvK58(4$J9k' );
define( 'LOGGED_IN_KEY', '}4Kxl65OpMD*b!oeBtE7]=^%#.%Zo!s_aZn^] gaw&jdLATTi78VtRwCiLONZ|Br' );
define( 'NONCE_KEY', 'Y,.NJcYM2irW>2h=TZ]Dv45_yU! [qaP<r0,-^Z]>]>P SYmtWPz0&cY$>uM4t5' );
define( 'AUTH_SALT', 'b(!k*o(EL)dGBM[H)?]J(lV/QPT;W)lvFOASqD6bnY~)[%5RCyAC%cu=~`~^}BAD' );
define( 'SECURE_AUTH_SALT', 'g[]P:5c|8fL%8/YW?8qX#l:[_9D(-7CzhovYIjLBj,z23/P`N;|+0p^V}qFSM^oc' );
define( 'LOGGED_IN_SALT', 'Aq*+8H==G!1,{evw&1n+9Z3X5A</g9$!qI+PHYaMNgK`2)PfE8x^YiUR:lo&.mN6' );
define( 'NONCE_SALT', '}dw|%_P^F9ALb3Fr$9f!zjo6IpvOU<,Ocxx#vKr|[a[jic3v)/C~.l(PNj*4]Aqq' );

$table_prefix = 'wp_';
define( 'WP_DEBUG', false );

if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}
require_once ABSPATH . 'wp-settings.php';
"""

# Write wp-config.php
stdin, out, err = c.exec_command('cat > /www/wwwroot/skillxm.cn/public/wp-config.php << \'EOF\'\n' + wp_config + '\nEOF')
print('Write config:', err.read().decode().strip() if err.read() else 'OK')

# Set permissions
stdin, out, err = c.exec_command('chown www:www /www/wwwroot/skillxm.cn/public/wp-config.php && chmod 644 /www/wwwroot/skillxm.cn/public/wp-config.php')
print('Permissions:', err.read().decode().strip() if err.read() else 'OK')

# Verify
stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/public/wp-config.php')
print('Verify:', out.read().decode().strip())

c.close()