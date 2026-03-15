# VocabBook 中的 FSRS 记忆算法复刻日记
> 本项目为个人学习开发的**非商用项目**，仅用于记忆算法的学习与实践，不涉及任何商业用途。  
> 其中 FSRS 算法的部分源自（部分改编自） [FSRS4Anki](https://github.com/open-spaced-repetition/fsrs4anki)，遵循其开源协议。

最后更新：2026-3-15

## 2026-03-15
完成了基础 UI 和 csv 管理函数的部分开发，现在需要一套记忆算法运用于 VocabBook。  
现在有几大主流算法，我完全不需要自己整一套记忆算法，因为那样的算法既没有经过科学验证而且写起来没有一个目标。  
- SM-2 算法作为经典一派，虽然好用但是没有严格的数学证明，无法精确地预测每个人不同的记忆曲线；
- SSP-MMC 算法过于复杂庞大，一步到位的难度较大。

**最终选择了 FSRS 作为当前的构建目标。**

### FSRS
官方项目介绍：[FSRS4Anki Wiki](https://github.com/open-spaced-repetition/fsrs4anki/wiki)  
算法介绍：[The Algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)

### 算法中用到的符号
- $R$：可检索性（回忆概率）
- $S$：稳定性（对应 $R = 90\%$ 时的间隔）
  - $S_r$：回忆后新的稳定性
  - $S_f$：遗忘后新的稳定性
- $D$：难度（$D \in [1, 10]$）
- $G$：评分（Anki 中的评分等级）
  - $1$: 再次
  - $2$: 困难
  - $3$: 良好
  - $4$: 容易

这套算法描述是我在 fsrs4anki 中找到的，评分项为 Anki 中用户对一个记忆点打出的等级，这一项后续可能不会复刻。

### 算法关键

#### FSRS v4

##### 为什么选择 v4
到我访问这个介绍文档的时候，最上面的是 FSRS-6，问了下豆包，巴啦啦说了一堆，摘取一下重要的话：
> 简单说：
> - FSRS v4：是「够用且易实现」的 “黄金版本”—— 覆盖背单词的核心场景（跨天复习、答对 / 答错更新记忆状态、计算最优间隔），公式 / 参数数量适中，新手能 hold 住；
> - FSRS-5/6：是对 v4 的 “精准优化”，新增的公式都是为了适配「同一天重复复习」「不同用户记忆衰减差异」等边缘场景，核心逻辑和 v4 完全一致，只是更精细。

豆女士分析了一堆，反正现阶段用 v4 是最好的。

好的，我们回到官方项目介绍下的 FSRS v4，快速链接 [FSRS v4](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm#fsrs-v4)。  
原文档写的都是英文，让豆包翻译一下然后粘在下面(自己还修改了下，可能与原文档有出入）。

> ##### 来源：FSRS4Anki Wiki - FSRS v4 官方文档
> ##### 默认参数
> [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61]
>
> ##### 公式说明
> $W_i$ 表示 $W[i]$。该版本使用 17 个参数。记忆状态由稳定性（S）和难度（D）共同表示。
>
> ---
>
> 首次评分后的初始稳定性：
> 
> $$S_0(G) = w_{G-1}.$$
>
> 例如：$S_0(1) = w_0$ 是第一次评分为 Again（再次）时的初始稳定性。第一次评分为 Easy（容易）时，初始稳定性为 $S_0(4) = w_3$。
>
> ---
>
> 首次评分后的初始难度：
> 
> $$D_0(G) = w_4 - (G - 3) \cdot w_5.$$
>
> 其中，第一次评分为 Good（良好）时，$D_0(3) = w_4$。
>
> ---
>
> 复习后的新难度：
> 
> $$D'(D, G) = w_7 \cdot D_0(3) + (1 - w_7) \cdot \bigl(D - w_6 \cdot (G - 3)\bigr).$$
>
> 它会先用 $D' = D - w_6 \cdot (G - 3)$ 计算临时难度，再通过均值回归 $w_7 \cdot D_0(3) + (1 - w_7) \cdot D'$ 进行修正，以避免出现“难度地狱（ease hell）”。
>
> ---
>
> 自上次复习 t 天后的可检索性:
> 
> $$R(t, S) = \left(1 + \frac{t}{9 \cdot S}\right)^{-1},$$
> 
> 其中，当 $t = S$ 时，$R(t, S) = 0.9$。
>
> 将目标回忆率代入上面公式中的 $R$ 并求解 $t$，即可得到下一次复习间隔：
> 
> $$I(r, S) = 9 \cdot S \cdot \left(\frac{1}{r} - 1\right),$$
> 
> 其中：当 $r = 0.9$ 时，$I(r, S) = S$。
>
> ---
>
> 复习成功后的新稳定性（用户按下 Hard、Good 或 Easy 视为复习成功）：
> 
> $$S'_r(D, S, R, G) = S \cdot \left(e^{w_8} \cdot (11 - D) \cdot S^{-w_9} \cdot \left(e^{w_{10} \cdot (1 - R)} - 1\right) \cdot w_{15}\,(\text{if } G = 2) \cdot w_{16}\,(\text{if } G = 4) + 1\right).$$
> 
> 我们用 SInc（稳定性增幅）表示：$SInc = \frac{S_r'(D, S, R, G)}{S}$，它等价于 Anki 里的复习系数。
>
> 1. $D$ 越大，$SInc$ 越小，这意味着，难度越高的内容，记忆稳定性提升越少。
> 2. $S$ 越大，$SInc$ 越小，这意味着，记忆越牢固，想要进一步提升稳定性就越困难。
> 3. $R$ 越小，$SInc$ 越大，这意味着，间隔效应会随时间累计。
> 4. 复习成功时，$SInc$ 永远大于或等于 1。
>
> 在 FSRS 中，复习延迟（超期复习）对间隔的影响如下：
> 
> 随着延迟增加，可检索性（R）下降。如果复习成功，根据上面的第3点，随后的稳定性（S）会更高。然而，与 SM-2/Anki 算法随延迟线性增加不同，随后的稳定性会收敛到一个上限，这取决于你的 FSRS 参数。
>
> 你可以在这个演示工具中调整参数：https://www.geogebra.org/calculator/ahqmqjvx.
> 
>  ---
> 
> 遗忘后的新稳定性（复习失败）：
> 
> $$S'_f(D, S, R) = w_{11} \cdot D^{-w_{12}} \cdot \left( (S+1)^{w_{13}} - 1 \right) \cdot e^{w_{14} \cdot (1-R)}.$$
> 
> 比如，在默认参数下，当 $D=2$，$R=0.9$ 时，则 $S'_f(S = 100) = 2 \cdot 2^{-0.2} \cdot \left( (100 + 1)^{0.2} - 1 \right) \cdot e^{1 \cdot (1 - 0.9)} \approx 3$ 并且 $S_f'(S=1) ≈ 0.3$。

##### 参数设定

项目构建初期给一个单词留出的数据结构有以下参数：
```text
"word", "phonetic", "meaning", "example", "example_trans",
"textbook", "unit", "review_count", "correct_count", "last_review"
```

为了应用 FSRS v4 算法，以下核心参数是必须的：
```text
"stability", "difficulty", "next_review	", "retrievability"
```

还可以有以下辅助参数：
```text
"wrong_count", "first_learn"
```

将新增的参数写入 utils/constants.py 下的 STANDARD_CSV_HEADERS。