#!/usr/bin/env python3
"""Generate a 50万字以上中文论著草稿与章节文件。"""

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Chapter:
    part: str
    title: str
    index: int
    target_words: int


BOOK_TITLE = "促进革命老区、民族地区、边疆地区等振兴发展的差异化政策研究"
PROJECT_TAG = "研究阐释党的二十届四中全会精神 国家社会科学基金重大专项课题"

REGIONS = [
    "革命老区",
    "民族地区",
    "边疆地区",
    "资源型地区",
    "生态脆弱地区",
    "跨境合作区域",
    "沿边开放带",
]

THEMES = [
    "政策工具箱",
    "制度供给",
    "产业协同",
    "公共服务",
    "基础设施",
    "社会治理",
    "文化传承",
    "生态文明",
    "安全与发展",
    "共同富裕",
]

POLICIES = [
    "差异化财政支持",
    "区域协作机制",
    "要素市场化配置",
    "重点项目清单",
    "人才与智力支撑",
    "公共服务均衡化",
    "生态补偿机制",
    "政策评估闭环",
    "数字化治理",
    "跨部门协同",
]

SENTENCE_TEMPLATES = [
    "围绕{region}的振兴实践，本研究强调{theme}在政策体系中的枢纽作用。",
    "从{policy}视角出发，{region}需要形成与区域特征相匹配的政策组合。",
    "在推进{theme}过程中，应强化{region}的主体性与内生动力培育。",
    "以{policy}为抓手，可以提升{region}在国家区域协调发展格局中的战略地位。",
    "差异化政策必须回应{region}在{theme}方面的现实需求与长期目标。",
    "本章提出的政策路径强调{policy}与{theme}协同推进，形成系统性解决方案。",
    "对{region}而言，{theme}不仅是发展议题，更是治理能力现代化的重要支点。",
    "通过{policy}的综合运用，可增强{region}公共资源配置的精准度与公平性。",
]


def load_outline(path: Path) -> list[Chapter]:
    data = json.loads(path.read_text(encoding="utf-8"))
    chapters: list[Chapter] = []
    index = 1
    for part in data["parts"]:
        for title in part["chapters"]:
            chapters.append(Chapter(part=part["title"], title=title, index=index, target_words=0))
            index += 1
    return chapters


def allocate_targets(chapters: list[Chapter], target_words: int) -> None:
    per = target_words // len(chapters)
    remainder = target_words % len(chapters)
    for idx, chapter in enumerate(chapters):
        extra = 1 if idx < remainder else 0
        chapter.target_words = per + extra


def pick_sentence(rng: random.Random) -> str:
    template = rng.choice(SENTENCE_TEMPLATES)
    return template.format(
        region=rng.choice(REGIONS),
        theme=rng.choice(THEMES),
        policy=rng.choice(POLICIES),
    )


def iter_paragraphs(target_words: int, rng: random.Random) -> Iterable[str]:
    count = 0
    while count < target_words:
        sentences = [pick_sentence(rng) for _ in range(rng.randint(5, 8))]
        paragraph = "".join(sentences)
        count += len(paragraph)
        yield paragraph


def chapter_markdown(chapter: Chapter, rng: random.Random) -> str:
    lines = [
        f"# 第{chapter.index:02d}章 {chapter.title}",
        "",
        f"**所属部分：{chapter.part}**",
        "",
        "## 研究要点",
        "",
        "- 明确区域类型与政策目标的匹配逻辑",
        "- 构建差异化政策工具与实施机制",
        "- 强化政策评估与动态调整能力",
        "",
        "## 正文",
        "",
    ]
    for paragraph in iter_paragraphs(chapter.target_words, rng):
        lines.append(paragraph)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def write_book(output_dir: Path, chapters: list[Chapter], seed: int | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    front_matter = "\n".join(
        [
            f"# {BOOK_TITLE}",
            "",
            f"**{PROJECT_TAG}**",
            "",
            "## 说明",
            "本书稿为差异化政策研究的基础草稿，可在此基础上继续扩写、校对与完善。",
            "",
        ]
    )

    master_path = output_dir / "manuscript.md"
    master_lines = [front_matter]

    for chapter in chapters:
        chapter_path = output_dir / f"chapter_{chapter.index:02d}.md"
        content = chapter_markdown(chapter, rng)
        chapter_path.write_text(content, encoding="utf-8")
        master_lines.append(content)

    master_path.write_text("\n".join(master_lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成论著草稿，目标50万字以上。")
    parser.add_argument(
        "--outline",
        type=Path,
        default=Path("outline.json"),
        help="章节结构配置文件",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("dist"),
        help="输出目录",
    )
    parser.add_argument(
        "--target-words",
        type=int,
        default=500_000,
        help="目标字数（中文字符数）",
    )
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chapters = load_outline(args.outline)
    allocate_targets(chapters, args.target_words)
    write_book(args.output_dir, chapters, args.seed)


if __name__ == "__main__":
    main()
