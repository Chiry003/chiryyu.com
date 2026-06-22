#!/usr/bin/env python3
"""Build the personal website from markdown articles with GEO optimization."""

import os, re, json

ARTICLES_DIR = '/Users/chiryyu/Documents/涉外律师/新文章'
SITE_DIR = '/Users/chiryyu/Documents/涉外律师/website'
ARTICLES_OUT = os.path.join(SITE_DIR, 'articles')
os.makedirs(ARTICLES_OUT, exist_ok=True)

META = {
    '01_泰国税务争议应对.md': {
        'slug': '01-thailand-tax-dispute', 'region': '泰国', 'tag': '税务合规',
        'date': '2026-06-07', 'desc': '泰国税务局2025年追缴税款超480亿泰铢，转移定价稽查飙升至35%。系统解析从稽查通知到行政诉讼的全流程应对策略。',
        'faq': [
            ('泰国税务局稽查的触发机制是什么？','大数据交叉比对、电子发票系统(e-Tax Invoice)和金融机构信息共享机制，使泰国税务局能精准锁定稽查目标。转移定价、常设机构认定、预提税是当前三大重点稽查领域。'),
            ('收到泰国税务稽查通知后应该怎么做？','收到通知后48小时内应成立内部应对小组、委托税务律师、启动文件隔离程序，避免向稽查官员提交未经审核的文件。'),
            ('泰国税务争议可以通过和解解决吗？','可以。税法税款本金不可减免，但罚金和附加费可通过和解减免。分期缴税是谈判重点。'),
            ('中资企业如何预防泰国税务争议？','建议做好五大支柱：关联交易文档提前准备、预约定价协议(APA)申请、常设机构风险主动管理、受益所有人合规文件、定期税务健康检查。'),
        ],
        'related': ['17-thailand-ma','09-thailand-factory-act','11-thailand-pdpa'],
    },
    '02_柬埔寨QIP申请实务.md': {
        'slug': '02-cambodia-qip', 'region': '柬埔寨', 'tag': '投资法',
        'date': '2026-06-08', 'desc': '2021年新投资法从"正面清单"转向"负面清单+激励分级"。拆解QIP从申请流程、税收优惠规则到持续合规义务的全流程操作要点。',
        'faq': [
            ('柬埔寨QIP申请需要多长时间？','文件齐全的情况下，柬埔寨发展理事会(CDC)审批QIP的周期约2-4个月。若涉及环保审批，可能延长至6个月以上。'),
            ('外资企业申请柬埔寨QIP的最低投资额是多少？','通常不低于50万美元，具体行业有差异。经济特区(SEZ)内的QIP项目门槛相对较低。'),
            ('柬埔寨QIP的税收优惠有哪些？','QIP项目享受3-9年的利润税免税期、进口设备免关税、特别折旧（40%资产原值）、股息预提税豁免等激励。'),
            ('柬埔寨QIP资格可能被撤销吗？','可以。提供虚假材料、连续两年未启动投资、违反环保/劳工法规、未经批准转让免税设备等均可能触发QIP撤销，需补缴全部已享受的税收优惠。'),
        ],
        'related': ['18-cambodia-sez','06-cambodia-construction','12-cambodia-labor-law'],
    },
    '03_泰国刑事拘留权利保护.md': {
        'slug': '03-thailand-criminal-defense', 'region': '泰国', 'tag': '刑事辩护',
        'date': '2026-06-09', 'desc': '从传唤到终审的12个关键节点，拘留阶段的六项核心权利，四大常见涉刑类型辩护要点，以及家属外部支持指南。',
        'faq': [
            ('中国公民在泰国被刑事拘留后有哪些权利？','享有律师在场权、翻译权、领事通知与探视权、保持沉默权、医疗保障权、禁止酷刑等六项核心权利。'),
            ('在泰国被拘留后如何申请保释？','保释由法院决定，需要保释金+2-4名泰籍担保人+交出护照+定期报到。外国人因逃跑风险评估较高，保释难度天然高于泰籍嫌疑人。'),
            ('中国驻泰国使领馆能提供什么帮助？','领事官员可以了解案情、协助聘请律师、联系家属、确保人道权益。但不能代理案件、提供具体法律意见或干预泰国司法程序。'),
        ],
        'related': ['01-thailand-tax-dispute','17-thailand-ma','13-malaysia-amla'],
    },
    '04_马来西亚PDPA执法风暴.md': {
        'slug': '04-malaysia-pdpa', 'region': '马来西亚', 'tag': '数据合规',
        'date': '2026-06-10', 'desc': '2024年PDPA修订后处罚上限提升至100万令吉+3年监禁。与GDPR和泰国PDPA横向对比，解析执法趋势与中资企业实操合规路径。',
        'faq': [
            ('马来西亚PDPA 2024修订的核心变化是什么？','数据保护官(DPO)强制化、数据泄露72小时强制通知、跨境数据传输机制多元化（SCC+BCR+白名单）、数据处理器直接责任、处罚上限提升至100万令吉+3年监禁。'),
            ('中资企业向中国传输马来西亚员工数据是否合规？','需满足条件之一：白名单、标准合同条款(SCC)、集团约束性规则(BCR)、或取得员工明确书面同意。目前中国不在白名单中。'),
        ],
        'related': ['11-thailand-pdpa','14-romania-gdpr','07-vietnam-data-localization'],
    },
    '05_罗马尼亚劳动法实务.md': {
        'slug': '05-romania-labor-law', 'region': '罗马尼亚', 'tag': '劳动法',
        'date': '2026-06-11', 'desc': '罗马尼亚劳动法受欧盟指令深度影响，对雇员保护远超中国标准。详解雇佣、解雇、加班、工会谈判的操作红线和合规要点。',
        'faq': [
            ('在罗马尼亚解雇员工有哪些法律限制？','解雇须基于法定理由并严格遵循程序。纪律解雇须在知悉违规后6个月内完成调查+书面告知+5天答辩期+工会监督。程序瑕疵即可导致解雇无效。'),
            ('罗马尼亚加班费的法律标准是什么？','加班须在30日内支付不低于正常时薪175%的加班费，或经员工书面同意以补休替代（60日内使用）。夜班/周末/公共假日工作通常为200%-300%。'),
        ],
        'related': ['14-romania-gdpr','12-cambodia-labor-law','16-indonesia-omnibus'],
    },
    '06_柬埔寨建筑施工许可.md': {
        'slug': '06-cambodia-construction', 'region': '柬埔寨', 'tag': '工程法',
        'date': '2026-06-12', 'desc': '施工许可不全→工程停工、备案无法通过→无法结算尾款→工程款拖欠→无力整改的恶性循环。拆解从三证体系到纠纷救济的全流程。',
        'faq': [
            ('柬埔寨建筑施工需要哪些许可证？','三证体系：开工许可证(Permit to Commence)、竣工证(Certificate of Completion)、使用证(Certificate of Occupancy)。缺任何一证均属违规。'),
            ('柬埔寨工程款纠纷如何解决？','可通过建设委员会调解、SIAC/HKIAC国际仲裁（柬埔寨已加入纽约公约）、或法院诉讼解决。推荐在合同中约定国际仲裁条款。'),
        ],
        'related': ['02-cambodia-qip','18-cambodia-sez','12-cambodia-labor-law'],
    },
    '07_越南数据本地化合规.md': {
        'slug': '07-vietnam-data-localization', 'region': '越南', 'tag': '数据合规',
        'date': '2026-06-13', 'desc': '第55号法令2026年生效，越南成为东盟数据本地化最严国家。详解触发本地化的"三步审查法"、跨境传输审批机制与中资企业合规路径。',
        'faq': [
            ('越南第55号法令的触发条件是什么？','三步审查法：①受监管主体（电信/互联网/增值服务企业）②处理三类数据（个人信息/服务关系/用户生成数据）③被公安部A05认定涉及网络犯罪且未整改。'),
            ('违反越南数据本地化要求的后果是什么？','可处2-5亿越南盾罚款；A05可要求封锁网站/应用、暂停域名和广告服务。严重者导致企业在越南市场直接"消失"。'),
        ],
        'related': ['04-malaysia-pdpa','11-thailand-pdpa','14-romania-gdpr','15-vietnam-investment-law'],
    },
    '08_印尼IKN投资法律框架.md': {
        'slug': '08-indonesia-ikn', 'region': '印尼', 'tag': '投资法',
        'date': '2026-06-14', 'desc': 'IKN总投资预估300亿美元，OIKN享有超常规权力。解析外资准入的"超国民待遇"、土地征收法律争议与PPP模式的四种架构。',
        'faq': [
            ('外资在印尼IKN可以100%持股吗？','在建筑/数字基础设施/可再生能源/医疗/教育等领域，外资可在IKN区域内100%持股，享受"超国民待遇"。但战略国防和大众媒体仍受限。'),
            ('IKN的投资优惠有哪些？','建筑权(HGB)最长80年、耕作权(HGU)最长95年、OIKN一站式审批、特殊PPP合同模式、税收优惠等。'),
        ],
        'related': ['16-indonesia-omnibus','15-vietnam-investment-law','02-cambodia-qip'],
    },
    '09_泰国工厂法工业用地合规.md': {
        'slug': '09-thailand-factory-act', 'region': '泰国', 'tag': '行政合规',
        'date': '2026-06-15', 'desc': 'DIW 2026年启动3类工厂全面合规审查。详解从选址五维审查、EIA审批时间线到排污许可持续达标的工业用地全流程合规要点。',
        'faq': [
            ('泰国工厂选址需要审查哪些维度？','五维审查：城市规划(颜色区)、环境保护区、工业区(IEAT)局内局外、社区法定最小距离、交通红线与基础设施。'),
            ('泰国3类工厂的EIA审批需要多长时间？','从TOR提交到EIA批准，通常需12-18个月。建议同步推进EIA和BOI申请以节约项目前期时间。'),
        ],
        'related': ['01-thailand-tax-dispute','17-thailand-ma','11-thailand-pdpa'],
    },
    '10_东盟六国仲裁执行全景.md': {
        'slug': '10-asean-arbitration', 'region': '东盟', 'tag': '争议解决',
        'date': '2026-06-16', 'desc': '东盟六国《纽约公约》覆盖全景比较。从公共政策抗辩到正当程序抗辩，从SIAC到CIETAC的机构选择策略，附仲裁条款设计黄金模板。',
        'faq': [
            ('东盟国家中仲裁裁决执行最可靠的是哪个？','新加坡是区域首选，SIAC裁决在六国认可度最高。马来西亚和泰国法院对仲裁持相对支持态度。印尼和越南的执行不确定性较高。'),
            ('仲裁条款应该如何设计？','推荐SIAC为默认仲裁机构，仲裁地新加坡，适用SIAC规则。须加入紧急临时措施条款和放弃上诉权条款。关联合同应统一适用同一仲裁条款。'),
        ],
        'related': ['19-malaysia-competition','20-china-odi','17-thailand-ma'],
    },
    '11_泰国PDPA数据合规.md': {
        'slug': '11-thailand-pdpa', 'region': '泰国', 'tag': '数据合规',
        'date': '2026-06-17', 'desc': 'PDPC从制度建设期转入执法深化期，2025年罚款超1.2亿泰铢。详解五大高风险场景与PDPA/GDPR/PIPL三方合规要点。',
        'faq': [
            ('泰国PDPA与中国PIPL的主要区别是什么？','PDPA以"同意"为核心基础，暂未将"正当利益"列为独立合法性基础；PIPL规定了更严格的跨境传输安全评估制度；PDPA的独特性在于有监禁条款。'),
            ('中资企业在泰国最常见的PDPA违规是什么？','五大高风险场景：员工数据跨境回传中国、APP过度收集用户数据、客户数据用于跨境营销、视频监控与人脸识别、供应商数据共享缺少数据处理协议。'),
        ],
        'related': ['04-malaysia-pdpa','14-romania-gdpr','07-vietnam-data-localization'],
    },
    '12_柬埔寨劳动法实务.md': {
        'slug': '12-cambodia-labor-law', 'region': '柬埔寨', 'tag': '劳动法',
        'date': '2026-06-18', 'desc': '2022年《工会法》降至15人可建工会，欠薪追溯期翻倍至6个月。拆解雇佣、解雇、罢工与NSSF合规全流程。',
        'faq': [
            ('柬埔寨员工解雇需要支付多少补偿？','按工龄计算工龄补偿金(Seniority Indemnity)，每工作满一年支付15天工资。2022年修法将欠薪追溯期从3个月翻倍至6个月。'),
            ('柬埔寨工会的注册门槛是多少？','2022年新《工会法》规定，15名工人即可注册成立工会（原为7人），但需在劳动部注册登记。合法罢工须经15天通知+15天协商+7天投票的程序。'),
        ],
        'related': ['05-romania-labor-law','18-cambodia-sez','06-cambodia-construction'],
    },
    '13_马来西亚AMLA反洗钱合规.md': {
        'slug': '13-malaysia-amla', 'region': '马来西亚', 'tag': '刑事合规',
        'date': '2026-06-19', 'desc': '2024年AMLA修订引入公司刑事责任倒置，FATF灰名单压力推动执法升级。详解可疑交易报告、CDD义务与企业合规体系设计。',
        'faq': [
            ('马来西亚AMLA下公司刑事责任的标准是什么？','2024年修订引入责任倒置——公司须证明已建立"充分合规程序"方可免责。洗钱罪最高15年监禁。可疑交易须在交易发生后5个工作日内报告。'),
            ('中资企业在马来西亚哪些行为容易触发AMLA？','关联方转移定价、现金交易超过5万令吉、多层SPV境外架构、跨境大额资金转移无商业实质等均属高风险行为。'),
        ],
        'related': ['04-malaysia-pdpa','19-malaysia-competition','03-thailand-criminal-defense'],
    },
    '14_罗马尼亚GDPR数据保护.md': {
        'slug': '14-romania-gdpr', 'region': '罗马尼亚', 'tag': '数据合规',
        'date': '2026-06-20', 'desc': 'ANSPDCP累计处罚超800万欧元。对比GDPR/PIPL/PDPA三方差异，解析CCTV监控、员工数据跨境、电商Cookie四大高风险场景。',
        'faq': [
            ('罗马尼亚GDPR执法有多严？','ANSPDCP自2018年以来已作出450+项处罚决定，罚金总额超800万欧元。工厂CCTV违规和员工数据跨境传输是两大执法重点。'),
            ('中资企业在罗马尼亚如何合规处理员工数据？','须指定DPO、对摄像头进行CCTV告知、向中国传输员工数据须签署SCC或BCR、跨境传输前进行数据保护影响评估(DPIA)。'),
        ],
        'related': ['04-malaysia-pdpa','11-thailand-pdpa','05-romania-labor-law'],
    },
    '15_越南投资法外资准入.md': {
        'slug': '15-vietnam-investment-law', 'region': '越南', 'tag': '投资法',
        'date': '2026-06-21', 'desc': '2020年《投资法》实施负面清单制度，IRC与ERC双轨并行。解析外资持股上限、两步并购审批与代持安排无效化的最高法院判例。',
        'faq': [
            ('越南外资企业注册需要哪些证书？','双轨制：投资登记证书(IRC)+企业登记证书(ERC)。并购交易还需额外完成并购审批——涉及有条件行业的目标公司需要两步审批。'),
            ('越南哪些行业限制外资持股？','广告(不超过49%)、运输(不超过49%-51%)、电信(不超过49%-65%，但需外方为WTO成员国实体)、教育(不超过本地需求的一定比例)等行业均有上限。'),
        ],
        'related': ['07-vietnam-data-localization','08-indonesia-ikn','16-indonesia-omnibus'],
    },
    '16_印尼综合法Omnibus.md': {
        'slug': '16-indonesia-omnibus', 'region': '印尼', 'tag': '投资法',
        'date': '2026-06-22', 'desc': '2023年《创造就业综合法》重塑印尼投资生态。OSS-RBA简化许可、遣散费上限调整、环评简化、HGB延至80年——外资影响全解析。',
        'faq': [
            ('印尼Omnibus Law对外资最大的利好是什么？','通过OSS-RBA简化经营许可、外资建筑权(HGB)延长至80年、废除负面清单改为优先领域制度、劳动法遣散费从43倍上限降至25倍。'),
            ('Omnibus Law对劳工保护有何变化？','遣散费总额上限从43倍月薪降至25倍；固定期限合同从最长3年延至5年；外包限制放宽；最低工资公式与经济增长率挂钩。'),
        ],
        'related': ['08-indonesia-ikn','15-vietnam-investment-law','05-romania-labor-law'],
    },
    '17_泰国并购M&A实务.md': {
        'slug': '17-thailand-ma', 'region': '泰国', 'tag': '并购',
        'date': '2026-06-23', 'desc': '外商经营法限制如何影响交易架构？BOI/IEAT如何绕过FBA？10亿泰铢并购管制门槛、25%强制要约收购线——泰国M&A全流程指引。',
        'faq': [
            ('外资收购泰国公司最大的法律障碍是什么？','《外商经营法》(FBA)将多数行业列为清单三受限行业，外资持股须不高于49%。可通过BOI促进资格或IEAT工业区入驻来豁免FBA限制。'),
            ('泰国并购交易需要反垄断申报吗？','根据2017年《贸易竞争法》，并购后营业额超过10亿泰铢须向贸易竞争委员会申请事前审批。上市公司收购超过25%触发强制要约收购。'),
        ],
        'related': ['01-thailand-tax-dispute','09-thailand-factory-act','19-malaysia-competition'],
    },
    '18_柬埔寨经济特区SEZ.md': {
        'slug': '18-cambodia-sez', 'region': '柬埔寨', 'tag': '投资法',
        'date': '2026-06-24', 'desc': '24+个经济特区，SEZ内QIP享额外优惠。详解入驻流程、关税保税管理、劳工合规与西港特区中资工厂的14个月投产案例。',
        'faq': [
            ('柬埔寨经济特区(SEZ)相比区外有哪些优势？','进口设备/原材料免关税和增值税、增值税0%、简化海关手续、一站式行政服务、土地长期租赁权保障（50+25年）。'),
            ('柬埔寨有哪些主要的经济特区？','全国24+个SEZ，最受中资欢迎的是西哈努克港经济特区(SSEZ)、金边经济特区(PPSEZ)、大成经济特区等。SSEZ已有200+家企业入驻。'),
        ],
        'related': ['02-cambodia-qip','12-cambodia-labor-law','06-cambodia-construction'],
    },
    '19_马来西亚竞争法并购管制.md': {
        'slug': '19-malaysia-competition', 'region': '马来西亚', 'tag': '竞争法',
        'date': '2026-06-25', 'desc': '2025年马来西亚正式引入经营者集中申报制度。全球20亿+本地4000万令吉触发门槛，两阶段审查，罚金可达全球营业额10%。',
        'faq': [
            ('马来西亚经营者集中申报的触发门槛是什么？','全球合并营业额超20亿令吉，或其中一方在马来西亚营业额超4000万令吉、另一方在马来西亚营业额超4000万令吉或市场份额超20%。'),
            ('违反马来西亚并购管制的处罚是什么？','可处全球营业额的10%以下罚款、勒令拆分已完成交易、或处以每日罚款。Gun-jumping同样面临高额处罚。'),
        ],
        'related': ['17-thailand-ma','13-malaysia-amla','10-asean-arbitration'],
    },
    '20_中国ODI备案全流程.md': {
        'slug': '20-china-odi', 'region': '跨境', 'tag': 'ODI',
        'date': '2026-06-26', 'desc': '发改委11号令+商务部3号令+外汇登记，三轨并行。ODI备案、核准、报告全流程实操指引。',
        'faq': [
            ('ODI备案需要多长时间？','非敏感、投资额3亿美元以下项目：发改委备案7-20个工作日+商务部备案3-20个工作日+外汇登记约5个工作日。核准项目（敏感或超3亿美元）时间更长。'),
            ('哪些行业属于ODI敏感行业？','房地产、酒店、影城、娱乐业、体育俱乐部、枪支弹药、武器装备、跨境水资源开发、新闻传媒等。这些行业的ODI需核准而非备案。'),
        ],
        'related': ['02-cambodia-qip','15-vietnam-investment-law','08-indonesia-ikn'],
    },
    '21_柬埔寨税务制度合规.md': {
        'slug': '21-cambodia-tax', 'region': '柬埔寨', 'tag': '税务合规',
        'date': '2026-06-27', 'desc': '柬埔寨五大税种详解：利润税、预扣税、增值税、最低税、薪资税。拆解QIP税收优惠、转让定价合规、税务稽查应对与GDT数字化转型。',
        'faq': [('柬埔寨企业所得税税率是多少？','标准税率20%，石油/天然气和特定自然资源开采行业为30%。QIP项目可享受3-9年免税期，免税期届满后可适用较低的优惠税率。'),
                ('柬埔寨QIP免税期届满后适用什么税率？','QIP免税期届满后，按行业和投资活动分级适用加速税率表。最低税(1%年营业额)在免税期内豁免，免税期届满后恢复适用。'),
                ('柬埔寨税务稽查如何应对？','收到稽查通知后应立即委托当地税务律师，整理近3年的完整账簿和凭证，配合稽查官员的合法要求。切勿隐匿财务资料或转移公司资产——这在柬埔寨是刑事犯罪。')],
        'related': ['02-cambodia-qip','18-cambodia-sez','22-cambodia-land'],
    },
    '22_柬埔寨土地法外资路径.md': {
        'slug': '22-cambodia-land', 'region': '柬埔寨', 'tag': '土地法',
        'date': '2026-06-28', 'desc': '宪法第44条禁止外国人持有土地所有权。详解四种合法路径：长期租赁、经济土地特许、共管公寓、土地控股公司，以及代持陷阱的致命风险。',
        'faq': [('外国人能在柬埔寨购买土地吗？','不能。柬埔寨宪法第44条禁止外国人持有土地所有权。但外国人可通过长期租赁(50+25年)、经济土地特许、购买共管公寓一层以上单元等合法方式取得土地使用权。'),
                ('通过柬埔寨人代持土地有什么风险？','代持是无效且违法的手段。常见风险包括：代持人私下出售土地、代持人死亡继承人拒绝返还、柬政府打击代持时土地被没收。2019年后柬埔寨严打代持安排，涉案土地可能被冻结。')],
        'related': ['02-cambodia-qip','18-cambodia-sez','06-cambodia-construction'],
    },
    '23_柬埔寨知识产权保护.md': {
        'slug': '23-cambodia-ip', 'region': '柬埔寨', 'tag': '知识产权',
        'date': '2026-06-29', 'desc': '先申请原则下的商标抢注风险、专利审查的实务难点、边境执法的全新利器。蜜雪冰城商标抢注案深度复盘，中资品牌入柬前必修IP课。',
        'faq': [('柬埔寨商标注册采用什么原则？','先申请原则(First-to-File)。商标权授予最先提交申请的一方。在柬埔寨没有使用的商标同样可被注册——这使得"抢注"成为中资品牌入柬最常见的IP陷阱。'),
                ('中国商标在柬埔寨受保护吗？','中国商标注册在柬埔寨不自动受保护。需要通过马德里议定书指定柬埔寨或直接在柬埔寨商业部知识产权局(DIP)提交国家注册申请。')],
        'related': ['21-cambodia-tax','26-cambodia-digital','18-cambodia-sez'],
    },
    '24_柬埔寨外汇管理资金进出.md': {
        'slug': '24-cambodia-fx', 'region': '柬埔寨', 'tag': '外汇管理',
        'date': '2026-06-30', 'desc': '高度自由的柬埔寨外汇体制下暗藏合规玄机。利润汇回五步流程、交叉货币风险管控、NBC反洗钱报告义务、地下钱庄打击行动——中资企业资金管理的全流程指引。',
        'faq': [('柬埔寨有外汇管制吗？','柬埔寨实行高度自由化的外汇管理体制，无资本管制措施。根据1997年《外汇法》，利润、股息、资本利得、特许权使用费等均可自由汇出。但单笔大额汇款须向柬埔寨国家银行(NBC)报告。'),
                ('从柬埔寨向中国汇回利润需要什么手续？','标准流程：税务清算证明(GDT)→董事会分红决议→审计报告→银行汇款申请→中国外汇管理局报告。注意：必须先完成柬埔寨的税务清算，否则银行拒绝处理。')],
        'related': ['21-cambodia-tax','20-china-odi','02-cambodia-qip'],
    },
    '25_柬埔寨环境法环评合规.md': {
        'slug': '25-cambodia-environment', 'region': '柬埔寨', 'tag': '环境法',
        'date': '2026-07-01', 'desc': '2025年Prakas 4828重塑EIA分类制度。详解EIA审批流程、环境合约履约体系、碳信用机遇与中国工厂的环保红线——从$50,000罚款案说起。',
        'faq': [('柬埔寨哪些项目需要做EIA？','工业采矿、大型制造业工厂、经济特区(SEZ)、电力项目(≥10MW)、大型基础设施(公路/港口/机场)、涉及自然保护区的开发项目等。2025年Prakas 4828对小型矿业项目提供了1公顷以下的环评豁免。'),
                ('柬埔寨EIA审批需要多长时间？','从TOR提交到EIA批准，整体周期约12-18个月。TOR审批45-60个工作日，EIA报告编制3-6个月，专家委员会审批60-90个工作日。环评未获批前不得启动任何现场施工。')],
        'related': ['02-cambodia-qip','18-cambodia-sez','06-cambodia-construction'],
    },
    '26_柬埔寨数字经济电商法.md': {
        'slug': '26-cambodia-digital', 'region': '柬埔寨', 'tag': '数字经济',
        'date': '2026-07-02', 'desc': '130%移动渗透率+40%电商增速+监管真空期——柬埔寨数字经济的机遇窗口。电商法、支付监管、网络安全法草案、数据保护法展望，中资科技公司的进入策略全解析。',
        'faq': [('中国科技企业在柬埔寨开展电商业务需要什么许可？','依据2019年《电子商务法》和《消费者保护法》，在柬埔寨运营电商平台须向商务部注册、遵守七天无理由退货规则(消费者保护法第12条)、在网页显著位置公示经营主体信息和营业许可。外资可在柬埔寨100%持股科技公司。'),
                ('柬埔寨有个人数据保护法吗？','目前尚未颁布综合性的个人数据保护法。2026年，柬埔寨邮电部和商务部正在联合起草《个人数据保护法》草案，预计2026-2027年提交国会审议。企业当前应参照东盟数据保护框架和即将出台的法律草案进行合规准备。')],
        'related': ['04-malaysia-pdpa','07-vietnam-data-localization','11-thailand-pdpa'],
    },
    '27_柬埔寨破产法债权人保护.md': {
        'slug': '27-cambodia-insolvency', 'region': '柬埔寨', 'tag': '破产法',
        'date': '2026-07-03', 'desc': '2019年新《破产法》取代旧法，债权人权利显著增强。法定优先顺序、可撤销交易追溯期、破产申请作为谈判筹码——中资企业追讨债务的全套法律武器。',
        'faq': [('柬埔寨破产清偿的顺序是什么？','第一顺位：担保债权人(以其担保物价值为限)；第二顺位：破产管理费用(含司法管理官报酬)；第三顺位：欠付员工工资(超级优先——6个月上限)；第四顺位：税务机关税款；第五顺位：无担保债权人；最后：股东。'),
                ('债务人进入破产程序后，债权人还能追回资产吗？','可以。2019年《破产法》赋予司法管理官"撤销权"——法院可裁定撤销债务人在破产前特定期限内进行的低价交易(2年内)、偏袒性支付(6个月内)和欺诈性财产转移(无时间限制)。')],
        'related': ['24-cambodia-fx','21-cambodia-tax','10-asean-arbitration'],
    },
    '28_泰国破产重整企业拯救.md': {
        'slug': '28-thailand-bankruptcy', 'region': '泰国', 'tag': '破产重整',
        'date': '2026-07-04', 'desc': '泰国2016年新增SME简易重整、2018年采纳UNCITRAL跨国界破产示范法。重整计划如何制定、债权人如何保护自己、境内财产如何不被跨境转移——中资企业债务危机的法律应对全解析。',
        'faq': [('泰国破产重整程序的启动条件是什么？','债权人可申请：个人债务人欠款≥100万泰铢、企业债务人欠款≥200万泰铢。债务人可自行申请重整：债务总额≥1,000万泰铢(有限公司)或≥200万泰铢(SME)。法院受理后产生自动中止效力——所有债权追索程序立即暂停。'),
                ('在泰国，债权人可以申请债务人破产吗？','可以。只要债权总额≥200万泰铢(企业)或≥100万泰铢(个人)，债务人到期未偿还且在债权人催告后30日内未能支付或提供合理担保的，债权人即可向破产法院提起破产申请。')],
        'related': ['01-thailand-tax-dispute','17-thailand-ma','27-cambodia-insolvency'],
    },
    '29_越南劳动法外籍员工.md': {
        'slug': '29-vietnam-labor', 'region': '越南', 'tag': '劳动法',
        'date': '2026-07-05', 'desc': '30天提前公开招聘义务、配额制度下的外籍员工数量限制、2022年起的强制社保——2019年《劳动法》对中方派遣人员的三重管控，及2023年第70号令的最新调整。',
        'faq': [('中国员工在越南工作需要什么许可？','越南雇主须为外籍员工申请工作许可(Work Permit)。申请前提：该岗位已向越南本地求职者公开招聘至少30天仍无法招募到合适人选。工作许可有效期最长2年，可续期一次。免办工作许可的情形极为有限(如持股超过一定比例的出资人、董事会成员等)。'),
                ('违反越南外籍劳工规定有什么后果？','外籍员工个人：可被驱逐出境并列入入境黑名单。雇主企业：行政罚款、6个月至1年内不得从非越南籍国家招聘新劳工、在越南投资登记系统中的雇主评级降级(影响未来投资审批)。')],
        'related': ['12-cambodia-labor-law','05-romania-labor-law','15-vietnam-investment-law'],
    },
    '30_一带一路投资风险地图.md': {
        'slug': '30-bri-risk-map', 'region': '跨境', 'tag': '投资法',
        'date': '2026-07-06', 'desc': '六国（泰柬马越印尼罗马尼亚）九大法律维度横向对比表，+政治风险维度共十项尽调清单。从外资准入到争议解决，从税务到劳动，中资出海前的全维度法律风险评估框架。',
        'faq': [('中资企业出海投资前应该做哪些法律尽调？','十项核心尽调清单：①外资准入限制及国家安全审查机制 ②土地所有权和使用权 ③税收制度及投资激励 ④劳动法及外籍员工管理 ⑤环境影响评价(EIA)要求 ⑥外汇管制及利润汇回制度 ⑦争议解决机制(法院vs仲裁) ⑧知识产权保护水平 ⑨反腐败及刑事合规 ⑩政治风险及投资条约保护。'),
                ('东盟国家中哪些投资风险最高？','从法律不确定性角度：柬埔寨(法律体系仍在发展中)、印尼(政策频繁调整)、越南(法规执行标准不透明)。从政治风险角度：各国均处于中低水平，但需关注特定行业(如柬埔寨博彩业、印尼矿业)的政策突转风险。')],
        'related': ['20-china-odi','10-asean-arbitration','08-indonesia-ikn'],
    },
    '31_泰国工作签证与社保合规.md': {
        'slug': '31-thailand-work-permit', 'region': '泰国', 'tag': '劳动合规',
        'date': '2026-07-07', 'desc': '2025年查处外籍劳工违规案件2,847起，中籍员工违规437起增长28%。详解Non-B签证、工作许可、社保合规、BOI/IEAT绿色通道与突击检查应对策略。',
        'faq': [
            ('中国人在泰国工作需要什么签证和许可？','须持Non-B商务签证入境（90天），入境后30天内办理工作许可(Work Permit)。BOI企业可走快速通道3-5个工作日获批，SMART Visa持有者免办工作许可。'),
            ('泰国社保对外籍员工是强制性的吗？','是。2023年起所有在泰国合法工作的外国人（含工作许可持有者）均须参加泰国社会保障体系，不能以"已在中国缴纳五险一金"为由豁免。雇主承担5%+雇员5%。'),
            ('在泰国违反工作许可规定有什么后果？','个人：5,000-50,000泰铢罚款+驱逐出境+最长10年黑名单。雇主：10,000-100,000泰铢罚款，BOI企业可能被暂停/撤销优惠。'),
        ],
        'related': ['01-thailand-tax-dispute','09-thailand-factory-act','17-thailand-ma'],
    },
    '32_柬埔寨银行与金融监管.md': {
        'slug': '32-cambodia-banking', 'region': '柬埔寨', 'tag': '金融监管',
        'date': '2026-07-08', 'desc': 'NBC 2026年启动金融科技沙盒2.0，资本充足率提至15.5%。拆解四类银行牌照、MFI/PSI申请路径、CAFIU反洗钱执法趋势与中资金融机构的进入策略。',
        'faq': [
            ('外资可以在柬埔寨100%持股银行吗？','可以。柬埔寨银行体系对外资持完全开放态度，外资可100%持有柬埔寨银行牌照。但NBC要求母行评级不低于BBB(BBB/S&P)或Baa2(穆迪)，且须取得母国监管确认函。'),
            ('柬埔寨商业银行的最低资本要求是多少？','全能银行4000亿瑞尔(≈1亿美元)、商业银行1500亿瑞尔(≈3,750万美元)、专业银行300亿瑞尔(≈750万美元)、外资银行分行须拨入1亿美元运营资金。'),
        ],
        'related': ['21-cambodia-tax','24-cambodia-fx','26-cambodia-digital'],
    },
    '33_马来西亚劳动法外籍员工.md': {
        'slug': '33-malaysia-employment', 'region': '马来西亚', 'tag': '劳动法',
        'date': '2026-07-09', 'desc': '2026年《雇佣法》全面保护月薪4,000令吉以下员工。详解外籍员工四道准入审批、解雇正当理由制度、国内调查(DI)程序与EPF/SOCSO合规要点。',
        'faq': [
            ('马来西亚解雇员工需要什么程序？','须有"正当理由"(Just Cause)。因不当行为解雇须经国内调查(Domestic Inquiry)程序：发出Show Cause Letter→组建调查小组→听证会→作出结论。程序瑕疵可导致工业法院裁定解雇无效。'),
            ('中国员工在马来西亚工作须参加当地社保吗？','是。须参加EPF(公积金)和SOCSO(社会保障)。2024年起外籍员工可选择较低EPF费率(9%+11%)。中马尚无社会保障双边协议——意味着双重缴费风险。'),
        ],
        'related': ['12-cambodia-labor-law','05-romania-labor-law','29-vietnam-labor'],
    },
    '34_罗马尼亚公司法与外商投资.md': {
        'slug': '34-romania-company-law', 'region': '罗马尼亚', 'tag': '公司法',
        'date': '2026-07-10', 'desc': '2026年第32号法律引入实际受益人电子申报和CEISD审查扩展。拆解SRL/SA/分支机构设立全流程、外商投资安全审查触发条件与欧盟公司法的多层约束。',
        'faq': [
            ('外国人在罗马尼亚设立公司的最低注册资本是多少？','有限责任公司(SRL)最低注册资本为1列伊(≈0.2欧元)，但实践中建议注资不低于10,000欧元以维持商业信誉。股份公司(SA)最低注册资本90,000列伊(≈18,000欧元)。'),
            ('在罗马尼亚投资需要外商投资审查吗？','欧盟外投资者在罗投资超过200万欧元且涉及关键基础设施、关键技术、关键资源、敏感数据、国防、健康等行业的，须经CEISD审查。审查周期60个工作日。"抢跑"可导致交易无效+投资额10%罚款。'),
        ],
        'related': ['05-romania-labor-law','14-romania-gdpr','15-vietnam-investment-law'],
    },
    '35_越南税务与转让定价.md': {
        'slug': '35-vietnam-tax', 'region': '越南', 'tag': '税务合规',
        'date': '2026-07-11', 'desc': '2025年GDT转让定价稽查追缴16.8万亿越南盾（占追缴总额40%）。详解CIT/VAT/FCWT三大税种、三层转让定价文档体系、全球最低税冲击与税务争议应对。',
        'faq': [
            ('越南企业所得税的标准税率和优惠是什么？','标准税率20%。高科技/大规模制造可享受10%(15年)、15%(10年)等优惠税率，叠加"4免9减半"或"2免4减半"免税期。但全球最低税(GloBE)可能将有效税率补足至15%。'),
            ('越南转让定价稽查的重点是什么？','六大重点：持续亏损但仍扩大投资的FIE、利润率显著低于行业平均、向关联方支付高额服务费/许可费、无形资产转让、多层导管跨境交易、关联贷款高息或免息。未能按时提交转让定价文档的，GDT可自行"推定"交易价格。'),
        ],
        'related': ['01-thailand-tax-dispute','21-cambodia-tax','15-vietnam-investment-law'],
    },
    '36_印尼个人数据保护法.md': {
        'slug': '36-indonesia-pdp', 'region': '印尼', 'tag': '数据合规',
        'date': '2026-07-12', 'desc': '印尼UU PDP 2026年执法过渡期届满，LPDP启动首批执法行动。解析域外管辖、6项合法性基础、DPO强制任命、3×24小时泄露通知与年营收2%罚款——中资科技企业的数据合规新挑战。',
        'faq': [
            ('印尼PDP法有域外管辖效力吗？','有。UU PDP适用于：①在印尼境内处理数据；②在境外处理但产生印尼境内法律效果；③涉及印尼公民个人数据——无论数据处理者是否在印尼设有机构。'),
            ('印尼PDP的处罚有多严厉？','行政处罚最高达年营收的2%。刑事制裁最高6年监禁+60亿盾罚款（法人罚金可达个人3倍）。公司可因未尽防止犯罪义务被追究刑事责任（Superior Responsibility Doctrine）。'),
        ],
        'related': ['11-thailand-pdpa','04-malaysia-pdpa','07-vietnam-data-localization'],
    },
    '37_泰国公寓法与外国人购房.md': {
        'slug': '37-thailand-condominium', 'region': '泰国', 'tag': '房地产法',
        'date': '2026-07-13', 'desc': '中国买家以46.6%占比居泰国外籍购房者首位。详解49%外国人配额、FET Form资金汇入要求、代持致命风险、开发商违约救济与替代性持有结构的法律评估。',
        'faq': [
            ('外国人在泰国购买公寓有什么限制？','可合法持有公寓永久产权(Freehold)，但不得超过该公寓项目总出售面积的49%（"外国人配额"）。购房资金须从境外汇入泰国，并取得银行FET Form。土地绝对禁止外国人持有。'),
            ('泰国公寓"外国人配额"满了怎么办？','不可通过泰籍人士代持——代持属违法，可致交易无效+刑事追责+移民黑名单。替代方案：①30年租赁权(Leasehold)；②设立泰国公司(外资≤49%)以公司名义购买；③等待配额空出（其他外国业主出售）。'),
        ],
        'related': ['03-thailand-criminal-defense','11-thailand-pdpa','17-thailand-ma'],
    },
    '38_东盟跨境电商法律合规.md': {
        'slug': '38-asean-ecommerce', 'region': '东盟', 'tag': '数字经济',
        'date': '2026-07-14', 'desc': '东盟电商GMV达1,860亿美元，多国监管集中"收网"。六维度拆解：市场准入、海关税务（LVG/VAT代扣）、消费者保护、数据合规、知识产权、争议解决——中资电商平台的合规行动清单。',
        'faq': [
            ('印尼对跨境电商有什么特殊限制？','最严：社交媒体与电商分离(Permendag 31/2023)、跨境最低货值100美元、正面清单制度（禁止廉价纺织品/鞋类/电子产品跨境销售）。外资电商须设立PT PMA。'),
            ('东盟国家中哪些电商市场最开放？','从监管宽松度排序：柬埔寨>马来西亚>菲律宾>泰国>越南>印尼。柬埔寨电商监管仍处于早期阶段，是当前合规成本最低的窗口期市场。'),
        ],
        'related': ['07-vietnam-data-localization','11-thailand-pdpa','26-cambodia-digital'],
    },
    '39_FIDIC国际工程合同.md': {
        'slug': '39-fidic-contracts', 'region': '跨境', 'tag': '工程法',
        'date': '2026-07-15', 'desc': '东盟中资工程80%采用FIDIC合同。深度拆解十大攻防要害：Time Bar（28天索赔时效灭失）、工程师决定、不可预见条件、DLD误期赔偿、DAAB裁决约束力——程序即权利。',
        'faq': [
            ('FIDIC合同下索赔的"Time Bar"是什么意思？','承包商须在知晓索赔事件后28天内向工程师发出索赔通知，否则丧失索赔权利。2017版还要求在84天内提交"详细充分索赔"。这是FIDIC对承包商最无情的条款——"先干活后算账"的中国管理文化在此致命。'),
            ('FIDIC合同下的"工程师"是公平的吗？','理论上工程师应"中立"(2017版措辞从"公正"升级为"中立")，但实践中工程师由雇主聘任并支付报酬，天然倾向雇主利益。承包商须对所有口头指令进行书面确认(CVI)，所有决定不满须在时限内发出"异议通知"(NOD)——保留后续仲裁权利。'),
        ],
        'related': ['10-asean-arbitration','06-cambodia-construction','30-bri-risk-map'],
    },
    '40_跨境税务筹划与双边税收协定.md': {
        'slug': '40-cross-border-tax', 'region': '跨境', 'tag': '税务筹划',
        'date': '2026-07-16', 'desc': '约40%中资企业未充分利用DTA优惠。详解中国-东盟DTA优惠税率、控股架构税务逻辑、资本弱化规则、关联方贷款转让定价，以及全球最低税(GloBE)对传统税务筹划的颠覆。',
        'faq': [
            ('中国与东盟国家之间的股息预提税率是多少？','优惠税率通常为5%-10%（取决于持股比例和受益所有人资格）。如中国-新加坡为5%(持股≥25%)、中国-马来西亚为5%(持股≥25%)、中国-越南为5%(持股≥70%)。须满足"受益所有人"实质要求。'),
            ('全球最低税(GloBE)对中资海外投资有什么影响？','合并年营收超7.5亿欧元的跨国企业——海外子公司在低税率辖区的利润将被征收"补充税"补足至15%。传统"低税天堂中间控股"、"利息扣除最大化"、"无形财产利润转移"三大策略均受到根本性挑战。中等规模企业暂有几个年的过渡窗口期。'),
        ],
        'related': ['20-china-odi','21-cambodia-tax','35-vietnam-tax'],
    },
}

SKIP_LINES = {'余驰宇', '上海', '律师', '关注', '举报/反馈', '评论', '发表', '作者最新文章',
              '换一换', '扫码下载百度APP', '搜最新资讯、看热门视频', '设为首页',
              '我是余驰宇，中国执业律师', '请关注我，私信交流。'}

def normalize_markdown(text):
    text = re.sub(r'^##\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^###\s+', '', text, flags=re.MULTILINE)
    return text

def extract_toc(text):
    toc = []
    for line in text.split('\n'):
        line = line.strip()
        if re.match(r'^[一二三四五六七八九十]、', line):
            toc.append(('h2', line))
        elif line in ('引言', '结语', '问题的提出'):
            toc.append(('h2', line))
        elif re.match(r'^（[一二三四五六七八九十]）', line):
            toc.append(('h3', line))
    return toc

def generate_toc_html(toc):
    if len(toc) < 3: return ''
    html = '<nav class="article-toc"><h2>目录</h2><ol>\n'
    for level, title in toc:
        cls = 'toc-h2' if level == 'h2' else 'toc-h3'
        html += f'  <li class="{cls}"><a href="#{title}">{title}</a></li>\n'
    html += '</ol></nav>\n'
    return html

def generate_faq_schema(faq):
    if not faq: return ''
    items = ',\n'.join([
        f'    {{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faq
    ])
    return f'<script type="application/ld+json">\n{{\n  "@context":"https://schema.org",\n  "@type":"FAQPage",\n  "mainEntity":[\n{items}\n  ]\n}}\n</script>\n'

def generate_related_html(related_slugs, all_files, all_meta):
    """Generate related articles HTML."""
    html = '<nav class="related-articles"><h2>相关文章</h2><ul>\n'
    for slug in related_slugs:
        # Find the matching article
        for fname, meta in all_meta.items():
            if meta.get('slug') == slug:
                path = os.path.join(ARTICLES_DIR, fname)
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as fh:
                        title = fh.readline().replace('# ', '').strip()
                    html += f'  <li><a href="/articles/{slug}.html">{title}</a></li>\n'
                break
    html += '</ul></nav>\n'
    return html

def md_to_html(text):
    text = normalize_markdown(text)
    lines = text.split('\n')
    html = []
    in_ol = False; in_ul = False

    def close_lists():
        nonlocal in_ol, in_ul
        if in_ol: html.append('</ol>'); in_ol = False
        if in_ul: html.append('</ul>'); in_ul = False

    for line in lines:
        line = line.strip()
        if not line: close_lists(); continue
        if line in SKIP_LINES: continue
        if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}', line): continue
        if line.startswith('©') or line.startswith('京ICP'): continue
        if re.match(r'^\d+$', line) and len(line) <= 3: continue
        if '百度首页' in line or '余驰宇律师' in line: continue
        if len(line) < 5 and not re.match(r'^[一二三四五六七八九十]、', line): continue

        is_h2 = False
        if re.match(r'^[一二三四五六七八九十]、', line): is_h2 = True
        elif line in ('引言', '结语', '问题的提出'): is_h2 = True
        if is_h2:
            close_lists()
            html.append(f'<h2 id="{line}">{line}</h2>')
            continue

        if re.match(r'^（[一二三四五六七八九十]）', line):
            close_lists(); html.append(f'<h3>{line}</h3>'); continue

        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        if re.match(r'^\d+[\.\、]', line):
            if not in_ol: close_lists(); html.append('<ol>'); in_ol = True
            cleaned = re.sub(r'^\d+[\.\、]\s*', '', line)
            html.append(f'<li>{cleaned}</li>')
            continue
        if line.startswith('- '):
            if not in_ul: close_lists(); html.append('<ul>'); in_ul = True
            html.append(f'<li>{line[2:]}</li>')
            continue

        close_lists(); html.append(f'<p>{line}</p>')

    close_lists()
    return '\n'.join(html)


HTML_ARTICLE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="baidu-site-verification" content="codeva-clmOQd5j7H" />
<title>{title} | 余驰宇律师</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{region}法律,{tag},跨境投资,余驰宇律师">
<meta name="author" content="余驰宇">
<link rel="canonical" href="https://chiryyu.com/articles/{slug}.html">
<link rel="stylesheet" href="/css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RNSF9MHKRC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-RNSF9MHKRC');
</script>
<script>
var _hmt = _hmt || [];
(function() {{
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?4f699fb9163cce274dc69ba8316bb3e8";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
}})();
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "author": {{ "@type": "Person", "name": "余驰宇", "url": "https://chiryyu.com" }},
  "datePublished": "{date}T08:00:00+08:00",
  "dateModified": "{date}T08:00:00+08:00",
  "publisher": {{ "@type": "Person", "name": "余驰宇" }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://chiryyu.com/articles/{slug}.html" }}
}}
</script>
{faq_schema}
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav">
      <a href="/">首页</a>
      <a href="/articles/">文章</a>
      <a href="/about.html">关于</a>
    </nav>
  </div>
</header>

<article>
  <header class="article-header">
    <div class="article-region">{region} · {tag}</div>
    <h1>{title}</h1>
    <div class="article-meta">余驰宇 · {date}</div>
  </header>
  <div class="article-body">
<div class="article-summary">{desc}</div>
{toc}
{body}
{related}
  </div>
</article>

<footer class="site-footer">
  <p>© 2026 余驰宇律师 · <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;">📞 <a href="tel:+8615201911206">15201911206</a> · 微信 chiry003</p>
  <p style="margin-top:0.3rem;"><a href="/articles/">← 返回文章列表</a></p>
</footer>

</body>
</html>'''


# ===== BUILD =====
all_files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')])
cambodia_files = [f for f in all_files if '柬埔寨' in f]
other_files = [f for f in all_files if '柬埔寨' not in f]
files = cambodia_files + other_files

for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', '')
    region = meta.get('region', '跨境')
    tag = meta.get('tag', '法律')
    date = meta.get('date', '')
    desc = meta.get('desc', '')
    faq = meta.get('faq', [])
    related = meta.get('related', [])

    path = os.path.join(ARTICLES_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        raw = fh.read()

    lines = raw.split('\n')
    title = lines[0].replace('# ', '').strip()
    body_md = '\n'.join(lines[1:])
    body_md = re.sub(r'^---\s*$', '', body_md, flags=re.MULTILINE)
    body_md = re.sub(r'\|', ' ', body_md)

    body_normalized = normalize_markdown(body_md)
    toc = extract_toc(body_normalized)
    toc_html = generate_toc_html(toc)
    faq_schema = generate_faq_schema(faq)
    related_html = generate_related_html(related, files, META)
    body_html = md_to_html(body_md)

    html = HTML_ARTICLE.format(
        title=title, desc=desc, region=region, tag=tag,
        date=date, slug=slug, toc=toc_html, body=body_html,
        faq_schema=faq_schema, related=related_html,
    )

    out = os.path.join(ARTICLES_OUT, f'{slug}.html')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f'  ✅ {slug}.html (FAQ:{len(faq)} 内链:{len(related)})')


# ===== Articles Index =====
cards = []
for f in files:
    meta = META.get(f, {})
    slug = meta.get('slug', '')
    desc = meta.get('desc', '')
    path = os.path.join(ARTICLES_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        title = fh.readline().replace('# ', '').strip()
    cards.append(f'''    <a href="/articles/{slug}.html" class="article-card">
      <div class="card-meta">{meta.get('region','')} · {meta.get('tag','')}</div>
      <div class="card-title">{title}</div>
      <div class="card-desc">{desc}</div>
    </a>''')

with open(os.path.join(ARTICLES_OUT, 'index.html'), 'w', encoding='utf-8') as fh:
    fh.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="baidu-site-verification" content="codeva-clmOQd5j7H" />
<title>文章列表 | 余驰宇律师</title>
<meta name="description" content="余驰宇律师跨境投资法律实务文章合集，覆盖泰柬马罗越印六国。">
<link rel="stylesheet" href="/css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RNSF9MHKRC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-RNSF9MHKRC');
</script>
<script>
var _hmt = _hmt || [];
(function() {{
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?4f699fb9163cce274dc69ba8316bb3e8";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
}})();
</script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav"><a href="/">首页</a><a href="/articles/" class="active">文章</a><a href="/about.html">关于</a></nav>
  </div>
</header>
<main class="main-content">
  <h2 class="section-title">全部文章（共 {len(files)} 篇）</h2>
{chr(10).join(cards)}
</main>
<footer class="site-footer">
  <p>© 2026 余驰宇律师 · <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;">📞 <a href="tel:+8615201911206">15201911206</a> · 微信 chiry003</p>
</footer>
</body>
</html>''')
print('  ✅ articles/index.html')

# ===== About page =====
with open(os.path.join(SITE_DIR, 'about.html'), 'w', encoding='utf-8') as fh:
    fh.write('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="baidu-site-verification" content="codeva-clmOQd5j7H" />
<title>关于 | 余驰宇律师</title>
<meta name="description" content="余驰宇，中国执业律师，专注跨境投资法律实务。">
<link rel="stylesheet" href="/css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RNSF9MHKRC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-RNSF9MHKRC');
</script>
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?4f699fb9163cce274dc69ba8316bb3e8";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "余驰宇", "jobTitle": "律师",
  "description": "中国执业律师，专注跨境投资法律实务",
  "url": "https://chiryyu.com", "telephone": "+8615201911206",
  "knowsAbout": ["跨境投资法","泰国法律","柬埔寨法律","马来西亚法律","罗马尼亚法律","国际仲裁","税务合规"],
  "address": {"@type":"PostalAddress","addressLocality":"上海","addressCountry":"CN"}
}
</script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-title">余驰宇<span>律师</span></a>
    <nav class="site-nav"><a href="/">首页</a><a href="/articles/">文章</a><a href="/about.html" class="active">关于</a></nav>
  </div>
</header>
<section class="about-hero"><h1>余驰宇</h1><p>中国执业律师 · 跨境投资法律实务</p></section>
<main class="about-content">
  <h2>执业领域</h2>
  <p>余驰宇，中国执业律师，牵头柬埔寨、泰国、马来西亚、罗马尼亚等国当地律所的中国业务部，专注中资企业海外财产保护、重大诉讼/仲裁、税务问题处理、跨境保全与执行。</p>
  <h2>覆盖法域</h2>
  <ul>
    <li><strong>柬埔寨</strong> — QIP投资法、税务制度、土地法、劳动法、知识产权、外汇管理、环境法、经济特区、数字经济、破产法、建筑施工、赌场牌照</li>
    <li><strong>泰国</strong> — BOI投资、税务争议、M&A并购、PDPA数据合规、破产重整、工厂法、刑事辩护、EPC工程、反洗钱法</li>
    <li><strong>马来西亚</strong> — AMLA反洗钱、竞争法并购管制、PDPA数据合规、土地法、特许经营、中国仲裁执行</li>
    <li><strong>罗马尼亚</strong> — GDPR数据保护、劳动法、民事诉讼、储能投资、外资审查、国家援助规则</li>
    <li><strong>越南</strong> — 投资法外资准入、劳动法、数据本地化、跨境传输合规</li>
    <li><strong>印尼</strong> — Omnibus综合法、IKN新首都投资、外资准入</li>
    <li><strong>跨境</strong> — ODI备案全流程、东盟六国仲裁、一带一路风险地图</li>
  </ul>
  <h2>联系方式</h2>
  <p>📞 电话：<a href="tel:+8615201911206">15201911206</a></p>
  <p>💬 微信：<strong>chiry003</strong></p>
  <p>网站：<a href="https://shanghai.dacheng.com/lawyer_1/43.html">大成律师事务所</a></p>
</main>
<footer class="site-footer">
  <p>© 2026 余驰宇律师 · <a href="/">chiryyu.com</a></p>
  <p style="margin-top:0.5rem;">📞 <a href="tel:+8615201911206">15201911206</a> · 微信 chiry003</p>
</footer>
</body>
</html>''')
print('  ✅ about.html')

# ===== robots.txt =====
with open(os.path.join(SITE_DIR, 'robots.txt'), 'w') as fh:
    fh.write('''User-agent: *
Allow: /
Sitemap: https://chiryyu.com/sitemap.xml
User-agent: GPTBot
Allow: /
User-agent: CCBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: Baiduspider
Allow: /
''')
print('  ✅ robots.txt')

# ===== sitemap =====
urls = ['https://chiryyu.com/', 'https://chiryyu.com/about.html', 'https://chiryyu.com/articles/']
for f in files:
    meta = META.get(f, {})
    urls.append(f"https://chiryyu.com/articles/{meta.get('slug', '')}.html")
with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in urls:
        fh.write(f'  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n')
    fh.write('</urlset>\n')
print('  ✅ sitemap.xml')

with open(os.path.join(SITE_DIR, 'CNAME'), 'w') as fh:
    fh.write('chiryyu.com')

print(f'\n✅ 全部20篇文章 GEO 优化完成！')
print(f'   - FAQ 结构化数据（AI搜索引擎优先抓取）')
print(f'   - TL;DR 摘要（每篇开头）')
print(f'   - 交叉内链（每篇3-4篇相关文章）')
print(f'   - 百度/Google 双统计')
print(f'   - robots.txt 开放所有 AI 爬虫')
