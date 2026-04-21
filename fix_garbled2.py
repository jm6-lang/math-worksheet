import subprocess, base64

garbled_files = [
    (129, '758a8a9936f1fb69999839a4cd42fedf534f21ee', 'https://pan.quark.cn/s/b3bf3381be57'),
    (130, '50e1dd2f58b136ee90a6a4ccb7e8b59cdeb14d6e', 'https://pan.quark.cn/s/e63b50e9015a'),
    (131, '69a2a5214d8f89843341fbed530d11ab2563628c', 'https://pan.quark.cn/s/c5d2aaf7e516'),
    (132, 'c1e64d97df0495a0150e5e747e3667a99f11a071', 'https://pan.quark.cn/s/af4527f7974d'),
    (133, 'c6eb780cdaec644c10aae351ae93e255a20d6016', 'https://pan.quark.cn/s/eabd1416b3ed'),
    (134, 'a294480984d5e905e5082ce91a3702774c2a7e59', 'https://pan.quark.cn/s/16a51bd663f3'),
    (135, 'ed77a7c235cc4efe9f3dcc8dad9910a8d3a0e797', 'https://pan.quark.cn/s/d24a3fb36173'),
    (136, '369437876585175057b4c284a66cc39a2d8fabe4', 'https://pan.quark.cn/s/aeb4c9bd7292'),
    (137, '261437cc84d917a23f1c634b27045bd9269f6ba2', 'https://pan.quark.cn/s/7ac17fc10fca'),
    (138, '517feb7659f87825c14a8849db321eab14208c4b', 'https://pan.quark.cn/s/21c3cc764f9b'),
    (139, 'd27c364518e8ae9b8c9057e6257854822469e27d', 'https://pan.quark.cn/s/a7049a5ccf84'),
    (140, '25cfe298eb24e0ffc49878a6e8f854252ac29c6d', 'https://pan.quark.cn/s/85a951dc657b'),
    (141, '02e5437a7e6aa0546c4a0db6e6cb6216b29c1e86', 'https://pan.quark.cn/s/8c714df70baf'),
    (142, 'fa9ba0d359b1d85a08378c90a4391d763ca8afe0', 'https://pan.quark.cn/s/dd76e37fd8bc'),
    (143, '80cbe48fadceaa4613127218702f66f0dc4277c6', 'https://pan.quark.cn/s/ef0a2faac6f8'),
    (144, '18cfbc181c44cbbb4be98c30730e3fcd34e50539', 'https://pan.quark.cn/s/c6e9eac10d79'),
]

ok_count = 0
fail_count = 0

for i, sha, url in garbled_files:
    title = 'Quark' + str(i)
    new_content = '---\ntitle: "' + title + '"\ndescription: "Quark netdisk resource"\n---\n\n# ' + title + '\n\n<Badge type="tip" text="Quark" />\n\n## Resource Link\n\n| Platform | Link |\n| :--- | :--- |\n| Quark | [Click to Download](' + url + ') |\n\n::: tip\nIf the link expires, please contact admin to update\n:::\n'

    encoded = base64.b64encode(new_content.encode('utf-8')).decode('ascii')

    r = subprocess.run(
        ['gh', 'api', 'repos/jm6-lang/resource-portal/contents/docs/movies/post_%03d.md' % i,
         '-X', 'PUT',
         '-f', 'content=' + encoded,
         '-f', 'message=fix: repair garbled title post_%03d' % i,
         '-f', 'sha=' + sha],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if r.returncode == 0:
        ok_count += 1
        print('OK post_%03d' % i)
    else:
        fail_count += 1
        print('FAIL post_%03d: %s' % (i, r.stderr[:100]))

print('\nTotal: %d OK, %d FAIL' % (ok_count, fail_count))
