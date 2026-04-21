import subprocess, base64

# Check music directory for corresponding files
# The commit says "音乐资源迁移到影视聚集区"
# Let's see what music files existed at that time

# Get music post files
result = subprocess.run(
    ['gh', 'api', 'repos/jm6-lang/resource-portal/contents/docs/music',
     '--jq', '.[] | select(.type == "file") | .name'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
music_files = [f for f in result.stdout.strip().split('\n') if f.startswith('post_')]
print(f'Music has {len(music_files)} post files')

# Check the last few to find music resources
music_posts = sorted([f for f in music_files if f.startswith('post_')], key=lambda x: int(x.split('_')[1].split('.')[0]))
print('Last 5:', music_posts[-5:] if music_posts else 'None')

# Now let's also check the garbled title encoding more carefully
# The garbled title is "澶稿厠缃戠洏"
# Let's try big5 to decode
garbled = '澶稿厠缃戠洏'
utf8_bytes = garbled.encode('utf-8')
print('UTF-8 bytes hex:', utf8_bytes.hex())

# Try Big5-HKSCS decoding
try:
    big5_result = utf8_bytes.decode('big5hkscs')
    print('Big5-HKSCS:', big5_result)
except:
    print('Not Big5-HKSCS')

# The bytes are: e6be b6e7 a8bf e58e a0e7 bc83 e688 a0e6 b48f
# These look like they could be valid GBK if we re-group differently
# e6 be b6 e7 a8 bf e5 8e a0 e7 bc 83 e6 88 a0 e6 b4 8f
# GBK pairs: (e6be=夸), (b6e7=克), (a8bf=网), (e58e=? no), (a0e7=? no)
# Hmm, let me try another grouping
# e6 beb6 e7a8 bfe5 8ea0 e7bc 83e6 88a0 e6b4 8f
# None of these work as GBK pairs

# What if the bytes were swapped (little-endian)?
import struct
