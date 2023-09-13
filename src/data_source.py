import json
import shutil
from pathlib import Path

import os

from .consts import *
from .log import logger


class ModIntepreted:
    def __init__(self):
        """主类"""
        self._all_source_passages: list[dict] = []
        self._all_mods_passages: dict[str, list[dict]] = {}

        self._only_source_passages: list[str] = []  # 方便查重，仅 passage 列表
        self._file_source_passages: dict[str, list] = {}  # 方便替换，整合每个文件中的 passage
        self._file_mods_passages: dict[str, dict] = {}  # 方便替换，整合每个文件中的 passage

    """ 运行前检查 """
    def pre_process(self):
        """运行前检查"""
        self._is_paths_exists()
        self._mkdirs()

    @staticmethod
    def _is_paths_exists():
        """路径是否存在"""
        if not DIR_SOURCE_REPO.exists():
            logger.error(f"游戏源码路径 {DIR_SOURCE_REPO} 不存在！请检查后再运行！")
            raise

    @staticmethod
    def _mkdirs():
        os.makedirs("mods", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("results", exist_ok=True)

    """ 获取游戏已有的所有段落 """
    def fetch_source_passages(self):
        """获取游戏已有的所有段落"""
        for root, dir_list, file_list in os.walk(DIR_SOURCE_REPO / "game"):
            for file in file_list:
                if not file.endswith(".twee"):
                    continue
                with open(Path(root) / file, "r", encoding="utf-8") as fp:
                    lines = fp.readlines()

                relative_file_name = str(Path(root) / file).split("game\\")[1]
                self._file_source_passages[relative_file_name] = []

                for idx, line in enumerate(lines):
                    if not line.startswith("::"):
                        continue
                    line = line.lstrip(":: ")
                    if "[" not in line:
                        self._all_source_passages.append({
                            "passage": line.strip(),
                            "file": relative_file_name,
                            "start_line": idx
                        })
                        self._only_source_passages.append(line.strip())
                        self._file_source_passages[relative_file_name].append({
                            "passage": line.strip(),
                            "start_line": idx
                        })
                        continue
                    for idx_, ch in enumerate(line):
                        if ch != "[":
                            continue
                        line = line[:idx_-1]
                        self._all_source_passages.append({
                            "passage": line,
                            "file": relative_file_name,
                            "start_line": idx
                        })
                        self._only_source_passages.append(line)
                        self._file_source_passages[relative_file_name].append({
                            "passage": line,
                            "start_line": idx
                        })
                        break

        with open(FILE_ALL_SOURCE_PASSAGES, "w", encoding="utf-8") as fp:
            json.dump(self._all_source_passages, fp, ensure_ascii=False, indent=2)
        with open(FILE_ONLY_SOURCE_PASSAGES, "w", encoding="utf-8") as fp:
            json.dump(self._only_source_passages, fp, ensure_ascii=False, indent=2)
        with open(FILE_FILE_SOURCE_PASSAGES, "w", encoding="utf-8") as fp:
            json.dump(self._file_source_passages, fp, ensure_ascii=False, indent=2)
        logger.info(f"原游戏段落提取完成，共 {len(self._all_source_passages)} 个！")

    """ 检查一下模组文件夹内容 """
    def validate(self):
        """检查一下模组文件夹内容"""
        self._validate_folder_structure()

    @staticmethod
    def _validate_folder_structure():
        """检查文件夹该有的和不该有的"""
        for author in os.listdir(DIR_MODS_ROOT):
            needed_flag = False
            extra_flag = False
            for dir_name in os.listdir(DIR_MODS_ROOT / author):
                if dir_name in {"game", "img", "modules"}:
                    needed_flag = True
                    continue
                extra_flag = True
            if not needed_flag:
                logger.warning(f"{author} 目录下缺少必要文件夹 img, game, module 中的一个或多个！")
                raise
            if extra_flag:
                logger.warning(f"{author} 目录下除了必要文件夹 img, game, module 外还有其他文件！")
                raise
        logger.info("游戏文件夹检查完毕！")

    def _validate_js_syntax(self):
        """TODO js语法"""

    def _validate_css_syntax(self):
        """TODO css语法"""

    """ 获取模组的所有段落 """
    def fetch_mods_passages(self):
        """获取模组的所有段落"""
        for author in os.listdir(DIR_MODS_ROOT):
            self._all_mods_passages[author] = []
            self._file_mods_passages[author] = {}
            for root, dir_list, file_list in os.walk(DIR_MODS_ROOT / author / "game"):
                file_exists = False
                for file in file_list:
                    if not file.endswith(".twee"):
                        continue

                    relative_file_name = str(Path(root) / file).split("game\\")[1]
                    self._file_mods_passages[author][relative_file_name] = []
                    if (DIR_SOURCE_REPO / "game" / relative_file_name).exists():
                        file_exists = True

                    with open(Path(root) / file, "r", encoding="utf-8") as fp:
                        lines = fp.readlines()

                    for idx, line in enumerate(lines):
                        if not line.startswith("::"):
                            continue
                        line = line.lstrip(":: ")
                        if "[" not in line:
                            self._all_mods_passages[author].append({
                                "passage": line.strip(),
                                "file": relative_file_name,
                                "start_line": idx,
                                "file_exists": file_exists
                            })
                            self._file_mods_passages[author][relative_file_name].append({
                                "passage": line.strip(),
                                "start_line": idx,
                                "file_exists": file_exists
                            })
                            continue
                        for idx_, ch in enumerate(line):
                            if ch != "[":
                                continue
                            line = line[:idx_ - 1]
                            self._all_mods_passages[author].append({
                                "passage": line,
                                "file": relative_file_name,
                                "start_line": idx,
                                "file_exists": file_exists
                            })
                            self._file_mods_passages[author][relative_file_name].append({
                                "passage": line,
                                "start_line": idx,
                                "file_exists": file_exists
                            })
                            break

        with open(FILE_ALL_MODS_PASSAGES, "w", encoding="utf-8") as fp:
            json.dump(self._all_mods_passages, fp, ensure_ascii=False, indent=2)
        with open(FILE_FILE_MODS_PASSAGES, "w", encoding="utf-8") as fp:
            json.dump(self._file_mods_passages, fp, ensure_ascii=False, indent=2)
        logger.info(f"所有段落提取完成，分别为：{', '.join(f'{author} - {len(lists)}个！' for author, lists in self._all_mods_passages.items())}")

    """ 检查模组段落有无重复、多余的 """
    def validate_passage(self):
        """检查模组段落有无重复、多余的"""
        for author, passage_infos in self._all_mods_passages.items():
            for info in passage_infos:
                if info["file_exists"]:  # 文件存在，检查有没有新建的
                    if info["passage"] not in self._only_source_passages:
                        logger.error(f"{author} 的 {info['file']} 文件中有多余段落: {info['passage']}！")
                elif info["passage"] in self._only_source_passages:
                    logger.error(f"{author} 的 {info['file']} 文件中有重复段落: {info['passage']}！")
        logger.info("重复段落与多余段落检查完毕！")

    """ 处理模组的所有段落 """
    def process_mods_passages(self):
        """处理模组的所有段落。重复的删除原文后拼接，新建的复制粘贴"""
        for author, authordata in self._file_mods_passages.items():
            for filename, passagedatas in authordata.items():
                os.makedirs((DIR_RESULTS / author / "game" / filename).parent, exist_ok=True)
                for passagedata in passagedatas:
                    if passagedata["file_exists"]:  # 要删原文
                        with open(DIR_SOURCE_REPO / "game" / filename, "r", encoding="utf-8") as fp:
                            lines = fp.readlines()
                        lines_copy = lines.copy()

                        delete_flag = False
                        for source_passagedata in self._file_source_passages[filename]:
                            if source_passagedata["passage"] == passagedata["passage"]:  # 要删的段落:
                                for idx, line in enumerate(lines):
                                    if idx == source_passagedata["start_line"]:
                                        delete_flag = True
                                        lines_copy[idx] = None
                                    elif delete_flag and line.startswith("::"):
                                        delete_flag = False
                                    elif delete_flag:
                                        lines_copy[idx] = None
                        with open(DIR_MODS_ROOT / author / "game" / filename, "r", encoding="utf-8") as fp:
                            mod_lines = fp.readlines()

                        lines_copy.extend(mod_lines)
                        with open(DIR_RESULTS / author / "game" / filename, "w", encoding="utf-8") as fp:
                            fp.writelines([_ for _ in lines_copy if _ is not None])

                    else:  # 不删原文，直接复制粘贴
                        shutil.copyfile(
                            DIR_MODS_ROOT / author / "game" / filename,
                            DIR_RESULTS / author / "game" / filename
                        )
        logger.info("模组的所有段落已处理完成！")

    """ 处理其他文件 """
    def process_mods_files(self):
        """处理其他文件"""
        for author in os.listdir(DIR_MODS_ROOT):
            if (DIR_MODS_ROOT / author / "img").exists():
                shutil.copytree(
                    DIR_MODS_ROOT / author / "img",
                    DIR_RESULTS / author / "img",
                    dirs_exist_ok=True
                )
            if (DIR_MODS_ROOT / author / "modules").exists():
                shutil.copytree(
                    DIR_MODS_ROOT / author / "modules",
                    DIR_RESULTS / author / "modules",
                    dirs_exist_ok=True
                )
        logger.info("图片等其他文件已处理完成！")

    """ 覆盖原游戏文件 """
    def cover_source_files(self, author: str):
        if (DIR_RESULTS / author / "game").exists():
            shutil.copytree(
                DIR_RESULTS / author / "game",
                DIR_SOURCE_REPO / "game",
                dirs_exist_ok=True
            )
        if (DIR_RESULTS / author / "img").exists():
            shutil.copytree(
                DIR_RESULTS / author / "img",
                DIR_SOURCE_REPO / "img",
                dirs_exist_ok=True
            )
        if (DIR_RESULTS / author / "modules").exists():
            shutil.copytree(
                DIR_RESULTS / author / "modules",
                DIR_SOURCE_REPO / "modules",
                dirs_exist_ok=True
            )
        logger.info("原游戏文件已覆盖完成！")


__all__ = [
    "ModIntepreted"
]