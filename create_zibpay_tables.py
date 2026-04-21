import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CREATE] Zibpay database tables manually')

# Create the order table (from order-class.php line 41-85)
sql = """USE wp_skillxm;

CREATE TABLE IF NOT EXISTS wp_zibpay_order (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id int(11) DEFAULT NULL COMMENT 'user id',
    ip_address varchar(50) DEFAULT NULL COMMENT 'ip address',
    product_id varchar(50) DEFAULT NULL COMMENT 'product id',
    post_id int(11) DEFAULT NULL COMMENT 'post id',
    post_author int(11) DEFAULT NULL COMMENT 'post author',
    order_num varchar(50) DEFAULT NULL COMMENT 'order num',
    order_price double(10, 2) DEFAULT '0.00' COMMENT 'order price',
    order_type varchar(50) DEFAULT '0' COMMENT 'order type',
    create_time datetime DEFAULT NULL COMMENT 'create time',
    pay_num varchar(50) DEFAULT NULL COMMENT 'pay num',
    pay_type varchar(50) DEFAULT '0' COMMENT 'pay type',
    pay_price double(10, 2) DEFAULT NULL COMMENT 'pay price',
    pay_detail longtext COMMENT 'pay detail',
    pay_time datetime DEFAULT NULL COMMENT 'pay time',
    referrer_id int(11) DEFAULT NULL COMMENT 'referrer id',
    rebate_price double(10, 2) DEFAULT '0.00' COMMENT 'rebate price',
    rebate_status varchar(50) DEFAULT '0' COMMENT 'rebate status',
    rebate_detail longtext COMMENT 'rebate detail',
    income_price double(10, 2) DEFAULT '0.00' COMMENT 'income price',
    income_status varchar(50) DEFAULT '0' COMMENT 'income status',
    income_detail longtext COMMENT 'income detail',
    status varchar(50) DEFAULT '0' COMMENT 'status',
    other longtext COMMENT 'other',
    PRIMARY KEY (id),
    KEY user_id (user_id),
    KEY post_id (post_id),
    KEY order_num (order_num),
    KEY status (status),
    KEY order_type (order_type),
    KEY pay_time_idx (pay_time, pay_type, pay_price, id),
    KEY post_author_idx (post_author, referrer_id, income_status, rebate_status, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='pay order';
"""

# For card_pass table, create a basic structure since the code is obfuscated
sql += """
CREATE TABLE IF NOT EXISTS wp_zibpay_card_pass (
    id int(11) NOT NULL AUTO_INCREMENT,
    card varchar(100) DEFAULT NULL COMMENT 'card number',
    price double(10,2) DEFAULT NULL COMMENT 'price',
    type varchar(50) DEFAULT NULL COMMENT 'type',
    days int(11) DEFAULT NULL COMMENT 'vip days',
    status varchar(50) DEFAULT '0' COMMENT '0-unused 1-used',
    create_time datetime DEFAULT NULL COMMENT 'create time',
    use_time datetime DEFAULT NULL COMMENT 'use time',
    user_id int(11) DEFAULT NULL COMMENT 'user id',
    other longtext COMMENT 'other',
    PRIMARY KEY (id),
    KEY card (card),
    KEY status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='card pass';

CREATE TABLE IF NOT EXISTS wp_zibpay_income (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id int(11) DEFAULT NULL COMMENT 'user id',
    price double(10,2) DEFAULT NULL COMMENT 'price',
    type varchar(50) DEFAULT NULL COMMENT 'type',
    status varchar(50) DEFAULT '0' COMMENT 'status',
    create_time datetime DEFAULT NULL COMMENT 'create time',
    other longtext COMMENT 'other',
    PRIMARY KEY (id),
    KEY user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='income';
"""

sftp = client.open_sftp()
f = sftp.file('/tmp/create_zibpay_tables.sql', 'w')
f.write(sql)
f.close()

stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/create_zibpay_tables.sql 2>&1')
print('Tables created:', stdout.read().decode('utf-8', errors='ignore').strip())

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_skillxm LIKE \'%zibpay%\';"')
print('Zibpay tables:', stdout.read().decode('utf-8', errors='ignore').strip())

# Test wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k -b /tmp/cookies.txt "https://127.0.0.1/wp-admin/" 2>&1 | grep -c "wp-admin"')
count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin match count: {count}')

# Test homepage for errors
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | grep -c "Warning\\|Fatal\\|Error"')
warnings = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage warnings/errors: {warnings}')

client.close()
print('[DONE]')