#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文章重写脚本 - 根据标题生成原创内容
部署到服务器运行: python3 /www/wwwroot/resource_site/auto_collect/rewrite_articles.py
"""

import pymysql
import random
import re
import time
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ============ 数据库配置 ============
DB_CONFIG = {
    'host': 'localhost',
    'user': 'wp_user',
    'password': 'gMshA29CshK5',
    'database': 'wp_skillxm',
    'charset': 'utf8mb4'
}

# ============ 分类写作风格配置 ============
CATEGORY_CONFIG = {
    '教育资源': {
        'angles': [
            '学习方法与实践指南',
            '从入门到精通的系统路径',
            '高效学习策略与资源推荐',
            '实战技巧与常见误区',
            '课程评价与学习规划'
        ],
        'sections': ['学习背景', '核心内容解析', '实用学习建议', '常见问题解答', '学习资源推荐'],
        'keywords': ['学习方法', '知识体系', '技能提升', '高效学习', '系统学习', '实践应用'],
        'cta': '如果你觉得这篇文章对你有帮助，欢迎收藏本站，我们持续更新各类学习资源和教程。'
    },
    '工具合集': {
        'angles': [
            '工具深度测评与对比',
            '效率提升实战指南',
            '工具选择与使用技巧',
            '从新手到高手的进阶之路',
            '必备工具清单与推荐'
        ],
        'sections': ['工具概述', '核心功能详解', '使用技巧与窍门', '适用场景分析', '替代方案对比'],
        'keywords': ['效率工具', '实用推荐', '使用技巧', '功能对比', '生产力提升', '最佳实践'],
        'cta': '工具在于善用，如果你发现更多好用的工具，欢迎关注我们的更新。收藏本站，不错过每一期工具推荐。'
    },
    '网赚项目': {
        'angles': [
            '副业赚钱的实战经验分享',
            '从零开始的创业指南',
            '赚钱思路与落地方法',
            '真实案例分析与复盘',
            '行业趋势与机会洞察'
        ],
        'sections': ['项目背景分析', '盈利模式拆解', '实操步骤详解', '风险提示与建议', '进阶发展方向'],
        'keywords': ['副业收入', '赚钱方法', '创业项目', '被动收入', '商业模式', '实操经验'],
        'cta': '互联网赚钱没有捷径，但方法和方向很重要。关注本站获取更多网赚项目和实战经验分享。'
    },
    '影视娱乐': {
        'angles': [
            '深度影评与作品解析',
            '观影指南与推荐清单',
            '影史经典回顾',
            '影视行业趋势观察',
            '文化价值与社会意义'
        ],
        'sections': ['作品概述', '剧情深度分析', '制作亮点评析', '观影感受与推荐', '同类型作品推荐'],
        'keywords': ['影视推荐', '影评分析', '经典作品', '观影指南', '深度解析', '文化价值'],
        'cta': '好作品值得被更多人看到。关注本站，我们持续为你推荐优质影视内容和深度解析。'
    },
    '渠道资源': {
        'angles': [
            '优质资源渠道深度挖掘',
            '资源获取的实用指南',
            '行业信息渠道整合',
            '效率提升的资源策略',
            '资源管理与利用方法'
        ],
        'sections': ['资源概述', '渠道详细分析', '使用方法指导', '资源管理技巧', '延伸资源推荐'],
        'keywords': ['资源渠道', '信息获取', '效率提升', '实用指南', '资源整合', '最佳实践'],
        'cta': '优质资源是效率的基础。关注我们，获取更多高质量渠道和资源推荐。'
    }
}

DEFAULT_CONFIG = {
    'angles': ['实用指南与经验分享', '从入门到精通', '核心要点与实践方法', '常见问题与解决方案'],
    'sections': ['背景介绍', '详细内容', '实用技巧', '注意事项', '总结建议'],
    'keywords': ['实用指南', '方法技巧', '经验分享', '最佳实践', '注意事项'],
    'cta': '更多优质内容请持续关注本站，我们定期更新各类实用资源和教程。'
}


# ============ 同义词替换库 ============
SYNONYM_MAP = {
    '优秀': ['出色', '卓越', '优质', '精良', '出众'],
    '帮助': ['助力', '协助', '促进', '支持', '推动'],
    '提升': ['提高', '增强', '加强', '改善', '优化'],
    '方法': ['方式', '途径', '策略', '技巧', '手段'],
    '重要': ['关键', '核心', '至关重要', '必不可少', '不可或缺'],
    '了解': ['理解', '掌握', '熟悉', '认知', '洞察'],
    '学习': ['钻研', '研习', '修习', '进修', '研读'],
    '使用': ['运用', '利用', '应用', '采用', '借助'],
    '需要': ['有必要', '必不可少', '不可或缺', '至关重要', '迫切需要'],
    '问题': ['挑战', '难题', '困境', '障碍', '考验'],
    '方法': ['方案', '策略', '路径', '手段', '技巧'],
    '效果': ['成效', '成果', '效益', '表现', '结果'],
    '推荐': ['推荐', '建议', '值得尝试', '不妨试试', '强烈推荐'],
    '简单': ['便捷', '轻松', '容易上手', '简便', '不复杂'],
    '专业': ['专业', '深入', '系统', '全面', '精细化'],
    '发展': ['成长', '进步', '演进', '变革', '升级'],
    '选择': ['挑选', '甄选', '抉择', '确定', '选取'],
    '实际': ['实践', '实操', '实战', '真实', '落地'],
    '资源': ['素材', '材料', '资产', '储备', '内容'],
}

# ============ 段落模板库 ============
INTRO_TEMPLATES = [
    '在当今数字化快速发展的时代，{topic}已经成为了越来越多人关注的焦点。无论你是初学者还是有一定经验的老手，掌握{topic}相关的知识和技能都能为你的个人成长和职业发展带来巨大的帮助。本文将围绕"{title}"这一主题，为你提供一份全面而实用的参考指南。',
    '随着互联网的持续发展和信息技术的不断进步，{topic}领域正在经历着前所未有的变革。越来越多的朋友开始关注并投入到{topic}的学习和实践中来。今天我们就来深入探讨"{title}"，希望能为大家提供有价值的参考和启发。',
    '说到{topic}，相信很多朋友都不陌生。在这个信息爆炸的时代，了解并掌握{topic}相关的知识显得尤为重要。本文将系统地介绍"{title}"的核心要点，帮助你快速建立认知框架，少走弯路。',
    '近期，{topic}相关的讨论热度持续攀升，很多朋友都在寻找靠谱的学习资源和实践方法。为了帮助大家更好地理解和应用"{title}"，本文将从多个维度进行深入分析，力求给你带来真正有价值的参考内容。',
    '很多读者朋友私信问我们关于{topic}的问题，可见大家对这个话题的热情非常高。今天我们就以"{title}"为切入点，为大家梳理一份详尽的指南，覆盖核心概念、实用技巧和常见误区。',
]

SECTION_TEMPLATES = [
    # 通用段落
    '{section_title}\n\n{paragraph}\n\n{paragraph}',
    '{section_title}\n\n{paragraph}\n\n{paragraph}\n\n{paragraph}',
    # 列表型
    '{section_title}\n\n{intro_sentence}\n\n{list_items}\n\n{paragraph}',
    # 对比型
    '{section_title}\n\n{paragraph}\n\n{key_point_1}\n\n{key_point_2}\n\n{summary_sentence}',
]

PARAGRAPH_STARTERS = [
    '从实际应用的角度来看，', '根据行业经验来看，', '深入分析可以发现，',
    '值得注意的是，', '从专业角度来说，', '结合实际情况来看，',
    '实践证明，', '经过大量案例验证，', '从效率优化的角度，',
    '站在用户的角度，', '客观地讲，', '综合多方面因素，',
]

PARAGRAPH_MIDDLES = [
    '这一点在{topic}领域尤为突出。{topic}的快速发展带来了诸多机遇和挑战，需要我们保持学习和适应的态度。只有持续更新自己的知识储备，才能在竞争中保持优势。',
    '很多从业者在实践过程中都深有体会，{topic}领域的知识更新速度非常快。因此，建立一个系统化的学习体系非常重要，它可以帮助我们更有条理地吸收新知识。',
    '在深入了解{topic}的过程中，我们会发现，最有效的方式是将理论与实践紧密结合。单纯的理论学习容易流于表面，而缺乏理论指导的实践又容易迷失方向。',
    '{topic}领域的优秀从业者都有一个共同的特点，那就是善于总结经验并不断迭代优化。每一次的实践都是一次宝贵的学习机会，关键在于我们是否能够从中提炼出有价值的方法论。',
    '对于{topic}的理解不应该停留在表面层次。真正的高手往往能够在看似普通的现象中发现深层的规律和逻辑，这正是他们能够持续产出高质量成果的根本原因。',
]

PARAGRAPH_ENDINGS = [
    '因此，在{topic}的实践过程中，建议大家保持开放的心态，勇于尝试新的方法和思路，同时也要善于总结和反思。',
    '总的来说，{topic}是一个值得持续投入精力的领域。希望以上的分享能够对大家有所帮助，也欢迎在评论区交流你的看法和经验。',
    '只要我们保持学习的热情和正确的方法，在{topic}领域取得进步并不是一件困难的事情。关键在于坚持和积累。',
    '以上就是我们对于{topic}相关话题的一些思考和总结。每个人的情况不同，建议结合自身实际情况灵活调整，找到最适合自己的方式。',
]

LIST_ITEM_TEMPLATES = [
    '要点一：{point}。这是{topic}中非常基础但极其重要的一环，建议花足够的时间去理解和掌握。',
    '要点二：{point}。在实际操作中，这个方面往往被很多人忽视，但它对最终效果的影响不可小觑。',
    '要点三：{point}。掌握好这一点，可以显著提升你在{topic}领域的专业度和竞争力。',
    '要点四：{point}。这是进阶阶段必须突破的难点，也是区分新手和高手的关键分水岭。',
    '要点五：{point}。在实践中灵活运用这一策略，往往能收到事半功倍的效果。',
]


def get_config(category):
    return CATEGORY_CONFIG.get(category, CATEGORY_CONFIG.get('未分类', DEFAULT_CONFIG))


def extract_keywords(title):
    """从标题提取关键词"""
    # 去除常见前缀
    title = re.sub(r'^(最新|超全|最全|超强|必备|精品|完整|终极|史上|2024|2025|2026)\s*', '', title)
    # 去除常见后缀
    title = re.sub(r'(合集|全集|收藏版|指南|教程|攻略|宝典|大全|精选|推荐|解析|详解|入门|进阶|实战|深度)$', '', title)
    # 分词（简单的中文分词）
    keywords = []
    # 提取有意义的词组
    patterns = [
        r'[\u4e00-\u9fff]{2,8}(?:类|站|网|工具|软件|资源|课程|教程|项目|方法|技巧|技能)',
        r'[\u4e00-\u9fff]{2,4}(?:运营|管理|设计|开发|制作|学习|分析|优化|推广|营销)',
        r'[A-Z][a-zA-Z\s&]{2,20}',  # 英文术语
        r'[\u4e00-\u9fff]{4,10}',  # 长中文词组
    ]
    for p in patterns:
        matches = re.findall(p, title)
        keywords.extend(matches)
    if not keywords:
        keywords = [title]
    return list(set(keywords))[:5]


def synonym_replace(text, ratio=0.15):
    """同义词替换，ratio控制替换比例"""
    words = list(SYNONYM_MAP.keys())
    count = max(1, int(len(words) * ratio))
    chosen = random.sample(words, count)
    for word in chosen:
        if word in text and random.random() < 0.5:
            replacement = random.choice(SYNONYM_MAP[word])
            text = text.replace(word, replacement, 1)
    return text


def generate_intro(title, category, config):
    """生成引言段落"""
    topic = extract_keywords(title)[0] if extract_keywords(title) else title
    template = random.choice(INTRO_TEMPLATES)
    angle = random.choice(config['angles'])
    
    # 在引言中加入写作角度
    intro = template.format(title=title, topic=topic)
    
    # 添加角度说明
    angle_intro = f'\n\n本文将从"{angle}"的角度展开讨论，力求为读者提供一份有深度、有价值的参考内容。'
    intro += angle_intro
    
    return synonym_replace(intro)


def generate_section(title, category, config, section_name, section_index, total_sections):
    """生成一个主体段落"""
    topic = extract_keywords(title)[0] if extract_keywords(title) else title
    keywords = config['keywords']
    
    # 选择段落模板
    template_type = random.choice(['normal', 'list', 'contrast'])
    
    if template_type == 'normal' and section_index < total_sections - 1:
        # 普通段落：2-3个自然段
        paragraphs = []
        # 开头
        starter = random.choice(PARAGRAPH_STARTERS)
        first_para = f'{starter}{topic}领域有非常多值得深入探讨的方面。' + random.choice(PARAGRAPH_MIDDLES).format(topic=topic)
        paragraphs.append(synonym_replace(first_para))
        
        # 中间
        mid_keyword = random.choice(keywords)
        mid_para = f'在{mid_keyword}方面，{topic}的实践者需要注意几个核心要点。首先，要建立正确的认知框架，理解{topic}的基本原理和运作机制。其次，要注重实际操作的规范性，避免因为不当操作而影响最终效果。最后，要养成定期复盘和优化的习惯，这样才能持续提升。'
        paragraphs.append(synonym_replace(mid_para))
        
        # 结尾
        if random.random() > 0.5:
            end_para = random.choice(PARAGRAPH_ENDINGS).format(topic=topic)
            paragraphs.append(synonym_replace(end_para))
        
        content = f'\n\n<h2>{section_index+1}. {section_name}</h2>\n\n'
        content += '\n\n'.join(paragraphs)
        
    elif template_type == 'list':
        # 列表型段落
        list_items = []
        list_points = [
            '建立系统化的认知体系',
            '掌握核心方法论和工具',
            '注重实践与理论结合',
            '持续学习并跟踪行业动态',
            '善于总结经验教训',
            '构建个人知识管理体系',
            '培养批判性思维能力',
            '注重效率和质量平衡',
        ]
        random.shuffle(list_points)
        
        content = f'\n\n<h2>{section_index+1}. {section_name}</h2>\n\n'
        content += f'以下是关于{topic}的几个关键要点，建议逐一了解和实践：\n\n'
        for i, point in enumerate(list_points[:random.randint(3, 5)]):
            item_template = random.choice(LIST_ITEM_TEMPLATES)
            content += f'<p><strong>{item_template.format(point=point, topic=topic)}</strong></p>\n\n'
        
    else:
        # 对比/分析型段落
        content = f'\n\n<h2>{section_index+1}. {section_name}</h2>\n\n'
        
        para1 = random.choice(PARAGRAPH_STARTERS)
        para1 += f'{topic}领域的实践中，我们经常需要在不同方案之间做出选择。每种方案都有其适用的场景和局限性，关键在于根据自身的实际情况来做出最优决策。'
        content += synonym_replace(para1) + '\n\n'
        
        key_kw = random.choice(keywords)
        para2 = f'从{key_kw}的角度来看，选择合适的路径需要考虑多方面因素：时间投入、学习成本、预期收益以及可持续性。建议大家在做出决定之前，先做好充分的调研和评估。'
        content += synonym_replace(para2) + '\n\n'
        
        para3 = random.choice(PARAGRAPH_ENDINGS).format(topic=topic)
        content += synonym_replace(para3)
    
    return content


def generate_conclusion(title, category, config):
    """生成总结段落"""
    topic = extract_keywords(title)[0] if extract_keywords(title) else title
    cta = config['cta']
    
    conclusion = f'\n\n<h2>总结</h2>\n\n'
    conclusion += f'通过以上的详细介绍和分析，相信大家对于"{title}"已经有了更加全面和深入的认识。'
    conclusion += f'{topic}是一个充满机遇的领域，只要我们保持学习的热情，善于总结和实践，就一定能够取得理想的成果。'
    conclusion += f'\n\n{cta}'
    
    return synonym_replace(conclusion)


def generate_article(title, category):
    """生成一篇完整的原创文章"""
    config = get_config(category)
    
    # 生成引言
    article = generate_intro(title, category, config)
    
    # 生成主体段落
    sections = config['sections']
    num_sections = random.randint(3, 5)
    chosen_sections = random.sample(sections, min(num_sections, len(sections)))
    
    for i, section in enumerate(chosen_sections):
        article += generate_section(title, category, config, section, i, num_sections)
    
    # 生成总结
    article += generate_conclusion(title, category, config)
    
    return article


def main():
    # 读取命令行参数
    start_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    print(f"[重写脚本] 开始处理，从第{start_id}篇开始，每批{batch_size}篇")
    
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 获取文章列表
    cursor.execute("""
        SELECT p.ID, p.post_title, COALESCE(t.name, '未分类')
        FROM wp_posts p
        LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
        LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id AND tt.taxonomy='category'
        LEFT JOIN wp_terms t ON tt.term_id = t.term_id
        WHERE p.post_type='post' AND p.post_status='publish'
        ORDER BY p.ID ASC
        LIMIT %s OFFSET %s
    """, (batch_size, start_id))
    
    articles = cursor.fetchall()
    
    if not articles:
        print("没有更多文章需要处理")
        cursor.close()
        conn.close()
        return
    
    success = 0
    fail = 0
    
    for idx, (post_id, title, category) in enumerate(articles):
        try:
            print(f"  [{start_id + idx + 1}] ID={post_id} [{category}] {title[:40]}...", end=' ')
            
            # 生成新内容
            new_content = generate_article(title, category)
            
            # 包装HTML
            html_content = f'<!-- 原创内容 -->\n{new_content}\n'
            
            # 更新数据库
            cursor.execute(
                "UPDATE wp_posts SET post_content = %s WHERE ID = %s",
                (html_content, post_id)
            )
            conn.commit()
            
            success += 1
            print(f"OK ({len(new_content)}字)")
            
            # 随机延迟，避免过快
            time.sleep(random.uniform(0.1, 0.3))
            
        except Exception as e:
            fail += 1
            print(f"FAIL: {e}")
            conn.rollback()
    
    cursor.close()
    conn.close()
    
    print(f"\n[完成] 成功: {success}, 失败: {fail}")
    print(f"下一批: python3 {sys.argv[0]} {start_id + batch_size} {batch_size}")
    
    # 记录进度
    progress = {
        'last_id': start_id + len(articles),
        'batch_size': batch_size,
        'success': success,
        'fail': fail,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    with open('/www/wwwroot/resource_site/auto_collect/rewrite_progress.json', 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
