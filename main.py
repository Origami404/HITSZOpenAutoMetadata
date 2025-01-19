from typing import Any, Callable, Iterable, Literal, NoReturn, Optional, override
from itertools import product, starmap
from dataclasses import dataclass
from abc import ABC, abstractmethod
import operator

type 可能未知[T] = Optional[T]
未知 = None

type 学位类型 = Literal["本", "硕", "博"]


@dataclass
class 国家专业:
    """国家本科专业目录上的条目"""

    类别: str
    名称: str
    代码: str


class 国家专业列表:
    # 目前在项目里管着的, 哈深能发出毕业证的专业
    # 代码查询: http://www.moe.gov.cn/srcsite/A08/moe_1034/s4930/202403/W020240319305498791768.pdf
    计算机 = 国家专业("计算机类", "计算机科学与技术", "080901")
    大数据 = 国家专业("计算机类", "数据科学与大数据技术", "080910T")
    通信 = 国家专业("电子信息类", "通信工程", "080703")
    光电 = 国家专业("电子信息类", "光电信息科学与工程", "080705")
    电子封装 = 国家专业("电子信息类", "电子封装技术", "080709T")
    集成电路 = 国家专业("电子信息类", "集成电路设计与集成系统", "080710T")
    自动化 = 国家专业("自动化类", "自动化", "080801")
    机器人 = 国家专业("自动化类", "机器人工程", "080803T")
    空天 = 国家专业("地球物理学类", "空间科学与技术", "070802")
    电气 = 国家专业("电气类", "电气工程及其自动化", "080601")
    能动 = 国家专业("能源动力类", "能源与动力工程", "080501")
    化学 = 国家专业("化学类", "化学", "070301")
    # ?
    # 机械 = 国家专业("机械类", "机械工程", "080201")
    机械 = 国家专业("机械类", "机械设计制造及其自动化", "080202")

    建筑 = 国家专业("建筑类", "建筑学", "082801")
    城乡规划 = 国家专业("建筑类", "城乡规划", "082802")
    经管 = 国家专业("经济学类", "经济学", "020101")
    会计 = 国家专业("工商管理类", "会计学", "120203K")


@dataclass
class 专业:
    年级: int
    毕业代码: str
    学位: 学位类型 = "本"

    def is_vaild(self) -> bool:
        # 配合学校各年级开设专业情况具体检查
        return True

    @classmethod
    def all(
        cls,
        毕业代码集合: Iterable[str],
        年级集合: Iterable[int],
        学位集合: Iterable[学位类型] = ("本",),
    ) -> Iterable["专业"]:
        return starmap(cls, product(年级集合, 毕业代码集合, 学位集合))

    @override
    def __hash__(self) -> int:
        return hash((self.年级, self.毕业代码, self.学位))


type 学年类型 = Literal["大一", "大二", "大三", "大四"]
type 学期类型 = Literal["秋", "春", "夏"]


@dataclass
class 上课时间:
    学年: 学年类型
    学期: 学期类型

    @classmethod
    def all(
        cls, 学年集合: Iterable[学年类型], 学期集合: Iterable[学期类型]
    ) -> Iterable["上课时间"]:
        return starmap(cls, product(学年集合, 学期集合))

    @override
    def __hash__(self) -> int:
        return hash((self.学年, self.学期))


type 绩点影响类型 = Literal["核心权重", "核心扣分", "GPA"]


@dataclass
class 课程属性记录:
    专业集: frozenset[专业]
    上课时间集: frozenset[上课时间]

    学分值: 可能未知[float]
    课时数: 可能未知[int]
    课程分类: frozenset[str]
    绩点影响: 可能未知[绩点影响类型]


@dataclass
class 课程:
    主课号: str
    包含的课的课号: frozenset[str]
    相似的课的课号: frozenset[str]

    课程名称: str
    其他名称: frozenset[str]

    记录: tuple[课程属性记录, ...]


def fset[T](*args: T) -> frozenset[T]:
    return frozenset(args)


def union[T](*args: Iterable[T]) -> frozenset[T]:
    s = set()
    return frozenset(s.union(*args))


# 快速访问
计算机: str = 国家专业列表.计算机.代码
自动化: str = 国家专业列表.自动化.代码
大数据: str = 国家专业列表.大数据.代码


大类_23计信 = frozenset(
    专业.all(
        (
            国家专业列表.计算机.代码,
            国家专业列表.大数据.代码,
            国家专业列表.通信.代码,
            国家专业列表.光电.代码,
        ),
        (2023,),
    )
)
大类_23自动化 = frozenset(
    专业.all(
        (
            国家专业列表.自动化.代码,
            国家专业列表.电气.代码,
        ),
        (2023,),
    )
)
大类_23机器人 = frozenset(
    专业.all(
        (
            国家专业列表.机器人.代码,
            国家专业列表.机械.代码,
            国家专业列表.电子封装.代码,
            国家专业列表.能动.代码,
        ),
        (2023,),
    ),
)

大类_24计信 = frozenset(
    专业.all(
        (
            国家专业列表.计算机.代码,
            国家专业列表.大数据.代码,
            国家专业列表.通信.代码,
            国家专业列表.光电.代码,
            国家专业列表.电子封装.代码,
            国家专业列表.集成电路.代码,
        ),
        (2024,),
    )
)
大类_24机器人 = frozenset(
    专业.all(
        (
            国家专业列表.自动化.代码,
            国家专业列表.机器人.代码,
        ),
        (2024,),
    )
)


大一秋 = 上课时间("大一", "秋")
大一春 = 上课时间("大一", "春")
大一夏 = 上课时间("大一", "夏")

大二秋 = 上课时间("大二", "秋")
大二春 = 上课时间("大二", "春")
大二夏 = 上课时间("大二", "夏")

大三秋 = 上课时间("大三", "秋")
大三春 = 上课时间("大三", "春")
大三夏 = 上课时间("大三", "夏")

大四秋 = 上课时间("大四", "秋")
大四春 = 上课时间("大四", "春")
大四夏 = 上课时间("大四", "夏")


def 年级范围(开始: int, 结束: int) -> Iterable[int]:
    return range(开始, 结束 + 1)


# 实例数据
元数据 = [
    课程(
        主课号="MATH1015A",
        包含的课的课号=fset(),
        相似的课的课号=fset(),
        课程名称="微积分A",
        其他名称=fset("高等数学A"),
        记录=(
            课程属性记录(
                专业集=union(
                    专业.all((自动化, 计算机, 大数据), 年级范围(2019, 2022)),
                    大类_23计信,
                    大类_23自动化,
                    大类_23机器人,
                    大类_24计信,
                    大类_24机器人,
                ),
                上课时间集=fset(大一秋),
                学分值=5.0,
                课时数=未知,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
        ),
    ),
    课程(
        主课号="PHYS1001",
        包含的课的课号=fset(),
        相似的课的课号=fset(),
        课程名称="大学物理",
        其他名称=fset(
            "大学物理IA", "大学物理IB", "大学物理XA", "大学物理XB", "大学物理II"
        ),
        记录=(
            # 原大学物理II
            课程属性记录(
                专业集=union(
                    专业.all((自动化, 计算机, 大数据), 年级范围(2019, 2022)),
                    大类_23计信,
                    大类_23自动化,
                    大类_23机器人,
                    大类_24计信,
                    大类_24机器人,
                ),
                上课时间集=fset(大二秋),
                学分值=未知,
                课时数=未知,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
            # 原大学物理IA 和 原大学物理IB
            课程属性记录(
                专业集=fset(*专业.all((自动化,), 年级范围(2019, 2022))),
                上课时间集=fset(大一春, 大二秋),
                学分值=4.0,
                课时数=未知,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
            # 现大学物理XA 和 现大学物理XB
            课程属性记录(
                专业集=union(
                    大类_23计信,
                    大类_23自动化,
                    大类_23机器人,
                ),
                上课时间集=fset(大一春),
                学分值=5.0,
                课时数=未知,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
            课程属性记录(
                专业集=union(
                    大类_23计信,
                    大类_23自动化,
                    大类_23机器人,
                ),
                上课时间集=fset(大二秋),
                学分值=4.0,
                课时数=未知,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
            # 现大学物理IA 和 现大学物理IB
            课程属性记录(
                专业集=fset(
                    *专业.all(
                        (
                            # 国家专业列表.材料.代码,
                            # 国家专业列表.土木.代码,
                            国家专业列表.化学.代码,
                        ),
                        年级范围(2023, 2024),
                    )
                ),
                上课时间集=fset(大一春, 大二秋),
                学分值=4.5,
                课时数=未知,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
        ),
    ),
    课程(
        主课号="EE2024",
        包含的课的课号=fset("EE1011A", "EE1011B", "EE1007", "EE1009"),
        相似的课的课号=fset(),
        课程名称="高等电路与电子分析",
        其他名称=fset("电路IA", "电路IB", "模拟电子技术基础", "数字电子技术基础"),
        记录=(
            # TODO: 还不知道怎么上的
        ),
    ),
    课程(
        主课号="WRIT0001",
        包含的课的课号=fset(),
        相似的课的课号=fset(),
        课程名称="写作与沟通",
        其他名称=fset(),
        记录=(
            课程属性记录(
                专业集=union(
                    大类_23计信,
                    大类_23自动化,
                    大类_23机器人,
                ),
                # TODO: 不知道啥时候上
                上课时间集=fset(),
                学分值=1.0,
                课时数=未知,
                课程分类=fset("必修", "文理通识"),
                绩点影响="核心权重",
            ),
        ),
    ),
    课程(
        主课号="ENGG1003",
        包含的课的课号=fset(),
        相似的课的课号=fset(),
        课程名称="工程训练（电子工艺实习）",
        其他名称=fset(),
        记录=(
            课程属性记录(
                专业集=fset(专业(2021, 计算机)),
                上课时间集=fset(大二秋),
                学分值=1.0,
                课时数=未知,  # 很短
                课程分类=fset("必修", "实验"),
                绩点影响="核心权重",
            ),
            课程属性记录(
                专业集=union(大类_23自动化),
                上课时间集=fset(大一夏),
                学分值=1.0,
                课时数=80,
                课程分类=fset("必修", "实验"),
                绩点影响="核心权重",
            ),
        ),
    ),
    课程(
        主课号="LANG100X",
        包含的课的课号=fset("LANG1006", "LANG1007", "LANG1008"),
        相似的课的课号=fset(),
        课程名称="大学英语",
        其他名称=fset("大学英语A", "大学英语B", "大学英语C"),
        记录=(
            课程属性记录(
                专业集=union(
                    大类_23自动化,
                    大类_23计信,
                    大类_23机器人,
                ),
                上课时间集=fset(大一秋, 大一春),
                学分值=2.0,
                课时数=32,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
            课程属性记录(
                专业集=union(
                    大类_23自动化,
                    大类_23计信,
                    大类_23机器人,
                ),
                上课时间集=fset(大二秋),
                学分值=1.0,
                课时数=24,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
        ),
    ),
    课程(
        主课号="PE100X",
        包含的课的课号=fset("PE1001", "PE1002"),
        相似的课的课号=fset(),
        课程名称="体育",
        其他名称=fset(),
        记录=(
            课程属性记录(
                专业集=union(
                    大类_23自动化,
                    大类_23计信,
                    大类_23机器人,
                ),
                上课时间集=fset(大一秋, 大一春),
                学分值=1.0,
                课时数=32,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
            课程属性记录(
                专业集=union(
                    大类_23自动化,
                    大类_23计信,
                    大类_23机器人,
                ),
                上课时间集=fset(大二秋, 大二春, 大三秋, 大三春),
                学分值=0.5,
                课时数=16,
                课程分类=fset("必修"),
                绩点影响="核心权重",
            ),
        ),
    ),
]


未知代表类型: Literal["全集", "空集"] = "全集"


class 过滤器(ABC):
    @abstractmethod
    def keep(self, record: 课程属性记录) -> bool:
        pass

    def 处理未知(self) -> bool:
        match 未知代表类型:
            case "全集":
                return True
            case "空集":
                return False
            case _:
                raise ValueError


@dataclass
class 集合过滤器(过滤器):
    集合: Literal["专业", "上课时间", "课程分类"]
    类型: Literal["存在任一", "存在所有", "均不存在于"]
    值: frozenset

    @override
    def keep(self, record: 课程属性记录) -> bool:
        target_set: frozenset
        match self.集合:
            case "专业":
                target_set = record.专业集
            case "上课时间":
                target_set = record.上课时间集
            case "课程分类":
                target_set = record.课程分类
            case _:
                raise ValueError

        match self.类型:
            case "存在任一":
                return any(target in target_set for target in self.值)
            case "存在所有":
                return all(target in target_set for target in self.值)
            case "均不存在于":
                return not any(target in target_set for target in self.值)
            case _:
                raise ValueError


@dataclass
class 数值过滤器(过滤器):
    数值: Literal["学分值", "课时数"]
    类型: Literal["不等于", "等于", "大于", "小于", "大于等于", "小于等于"]
    值: float | int

    @override
    def keep(self, record: 课程属性记录) -> bool:
        target_value: 可能未知[float] | 可能未知[int]
        match self.数值:
            case "学分值":
                target_value = record.学分值
            case "课时数":
                target_value = record.课时数
            case _:
                raise ValueError

        if target_value == 未知:
            return self.处理未知()

        op: Callable[[float | int, float | int], bool]
        match self.类型:
            case "不等于":
                op = operator.ne
            case "等于":
                op = operator.eq
            case "大于":
                op = operator.gt
            case "小于":
                op = operator.lt
            case "大于等于":
                op = operator.ge
            case "小于等于":
                op = operator.le
            case _:
                raise ValueError

        return op(target_value, self.值)  # type: ignore


@dataclass
class 枚举过滤器(过滤器):
    枚举: Literal["绩点影响"]
    类型: Literal["应该是", "不应该是"]
    值: frozenset

    @override
    def keep(self, record: 课程属性记录) -> bool:
        target_value: 可能未知[Any]
        match self.枚举:
            case "绩点影响":
                target_value = record.绩点影响
            case _:
                raise ValueError

        if target_value == 未知:
            return self.处理未知()

        match self.类型:
            case "应该是":
                return target_value in self.值
            case "不应该是":
                return target_value not in self.值
            case _:
                raise ValueError


class 逻辑表达式(ABC):
    @abstractmethod
    def __call__(self, courses: Iterable[课程]) -> Iterable[课程]:
        pass


class 逻辑与(逻辑表达式):
    过滤器们: tuple[过滤器]

    def __init__(self, *过滤器们) -> None:
        super().__init__()
        self.过滤器们 = 过滤器们

    def __call__(self, courses: Iterable[课程]) -> Iterable[课程]:
        def should_keep_course(course: 课程) -> bool:
            for f in self.过滤器们:
                for r in course.记录:
                    if not f.keep(r):
                        return False
            return True

        return filter(should_keep_course, courses)


# 暂时不设计顶层的逻辑或

# 查询器例子
查询_2023级计信大类内任何专业都要上的课 = 逻辑与(
    集合过滤器("专业", "存在所有", 大类_23计信),
)
查询_2023级自动化大类内可能要上的课 = 逻辑与(
    集合过滤器("专业", "存在任一", 大类_23自动化),
)
查询_2023级要以计算机专业毕业大二要上的考试课 = 逻辑与(
    集合过滤器("专业", "存在所有", fset(专业(2023, 计算机))),
    集合过滤器("上课时间", "存在任一", fset(大二秋, 大二春, 大二夏)),
    枚举过滤器("绩点影响", "应该是", fset("核心权重")),
)
查询_以计算机毕业的情况下23级要上但是22级不用上的课 = 逻辑与(
    集合过滤器("专业", "存在所有", fset(专业(2023, 计算机))),
    集合过滤器("专业", "均不存在于", fset(专业(2022, 计算机))),
)

if __name__ == "__main__":

    def test(prompt: str, query: 逻辑表达式) -> None:
        print(f"================== 测试 {prompt} ==================")
        for c in query(元数据):
            print(c.主课号, c.课程名称)

    test("2023级计信大类内任何专业都要上的课", 查询_2023级计信大类内任何专业都要上的课)
    test("2023级自动化大类内可能要上的课", 查询_2023级自动化大类内可能要上的课)
    test(
        "2023级要以计算机专业毕业大二要上的考试课",
        查询_2023级要以计算机专业毕业大二要上的考试课,
    )
    test(
        "以计算机毕业的情况下23级要上但是22级不用上的课",
        查询_以计算机毕业的情况下23级要上但是22级不用上的课,
    )
