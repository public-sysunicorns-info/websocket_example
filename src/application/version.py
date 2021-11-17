import os
import re
import json
from typing import Union, List

COMMIT_SHA_DEFAULT_LENGTH=6

def get_current_branch() -> Union[None, str]:
    if os.path.exists(path=".git/HEAD"):
        try:
            with open(".git/HEAD", 'r') as _file:
                _content = _file.read()
            _cp_regex = re.compile(r'refs\/heads\/([a-zA-Z0-9\/]+)')
            _branch_result = _cp_regex.search(_content)
            _branch = _branch_result.group(1)
            return _branch
        except Exception as e:
            return None
    else:
        return None

def get_current_commit(length=COMMIT_SHA_DEFAULT_LENGTH) -> Union[None, str]:
    _branch = get_current_branch()
    if _branch is not None:
        if os.path.exists(path=f".git/refs/heads/{_branch}"):
            with open(f".git/refs/heads/{_branch}", 'r') as _file:
                _content = _file.read().replace("\n", "")
            if length > 0:
                return _content[0:length]
            else:
                return _content
    else:
        return None

def get_current_tags() -> List[str]:
    _env_version = os.getenv("GITHUB_TAG", default=None)
    if _env_version is None:
        if os.path.exists(".git/refs/tags"):
            _current_commit = get_current_commit(-1)
            _tags_file_list = os.listdir(".git/refs/tags")
            _tags = []
            for _tag_file in _tags_file_list:
                with open(f".git/refs/tags/{_tag_file}") as _file:
                    _commit = _file.read().replace("\n","")
                if _commit == _current_commit:
                    _tags.append(_tag_file)
            return _tags
        else:
            return [_env_version]
    else:
        return []


def _calculate_version(full: bool=True) -> str:
    _branch = get_current_branch()
    _commit = get_current_commit()
    _tags = get_current_tags()

    if len(_tags) == 0:
        if full:
            return f"{_branch}-{_commit}"
        else:
            return f"{_branch}"
    elif len(_tags) == 1:
        if full:
            return f"{_tags[0]}-{_commit}"
        else:
            return f"{_tags[0]}"
    else:
        return f"warning_version_not_conform"

def get_version(full: bool=True) -> str:
    if full:
        return os.getenv("VERSION_LONG", _calculate_version(full=True))
    else:
        return os.getenv("VERSION", _calculate_version(full=False))


if __name__ == "__main__":
    _json_response = {
        "branch": str(get_current_branch()).replace("/","-"),
        "commit": get_current_commit(),
        "tags": get_current_tags(),
        "version": str(get_version(full=False)).replace("/","-"),
        "version-long": str(get_version()).replace("/","-")
    }
    print(
        json.dumps(_json_response)
    )
