import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Read current custom.css
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
current_css = stdout.read().decode('utf-8', errors='replace')

# Remove old search mobile styles and add new better ones
search_fix = '''

/* ============================================
   v8 Search Box - Larger on Mobile
   ============================================ */

/* Desktop search - keep as is */
.search-input-group {
    display: flex;
    align-items: stretch;
    background: #fff;
    border: 2px solid #FF5E52;
    border-radius: 50px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(255,94,82,0.2);
}

.search-input-group .input-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    padding-left: 20px;
}

.search-input-group .search-icon {
    color: #999;
    margin-right: 10px;
}

.search-input-group .search-field {
    border: none;
    outline: none;
    font-size: 16px;
    width: 100%;
    padding: 16px 10px;
    background: transparent;
}

.search-input-group .search-submit {
    background: linear-gradient(135deg, #FF5E52, #ff7b5e);
    color: #fff;
    border: none;
    padding: 16px 40px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.search-input-group .search-submit:hover {
    background: linear-gradient(135deg, #e54d42, #FF5E52);
}

/* Mobile search - BIGGER and stacked */
@media screen and (max-width: 768px) {
    .search-section {
        margin: 20px 0 !important;
    }
    
    .search-input-group {
        flex-direction: column;
        border-radius: 16px;
        border-width: 2px;
        gap: 0;
    }
    
    .search-input-group .input-wrapper {
        padding: 14px 16px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .search-input-group .search-field {
        font-size: 16px;
        padding: 8px 10px;
    }
    
    .search-input-group .search-submit {
        width: 100%;
        padding: 16px;
        font-size: 16px;
        font-weight: 700;
        border-radius: 0 0 14px 14px;
    }
    
    .search-input-group .search-icon {
        font-size: 18px;
    }
}

/* Extra small screens */
@media screen and (max-width: 400px) {
    .search-input-group .search-field {
        font-size: 15px;
    }
    
    .search-input-group .search-submit {
        padding: 14px;
        font-size: 15px;
    }
}
'''

# Append
new_css = current_css.rstrip() + search_fix

# Write
cmd = f"cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css << 'CSSEOF'\n{new_css}\nCSSEOF"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
err = stderr.read().decode('utf-8', errors='replace')
if err:
    print(f'ERROR: {err[:500]}')
else:
    # Verify
    stdin, stdout, stderr = ssh.exec_command('wc -l /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
    lines = stdout.read().decode().strip()
    print(f'OK - custom.css now {lines} lines')

ssh.close()
