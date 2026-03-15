from manim import *
import numpy as np


class HC(Scene):
    def construct(self):
        # 1. KHỞI TẠO ĐỒ THỊ
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 6, 1], axis_config={"include_tip": False}
        ).add_coordinates()

        def func(x):
            return 3 * np.exp(-((x - 2.5) ** 2)) + 5 * np.exp(-((x - 7.5) ** 2) / 2)

        graph = axes.plot(func, color=BLUE, stroke_width=4)
        self.add(axes, graph)

        # 2. KHỞI TẠO ĐIỂM BẮT ĐẦU
        start_x = 0.5
        curr_x = start_x
        curr_y = func(curr_x)

        x_tracker = ValueTracker(start_x)

        dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(), func(x_tracker.get_value())),
                color=YELLOW,
                radius=0.1,
            )
        )
        v_line = always_redraw(
            lambda: axes.get_vertical_line(dot.get_center(), color=YELLOW)
        )
        self.add(dot, v_line)

        counter = Integer(0).to_corner(UR)
        label_steps = Text("Iteration: ", font_size=24).next_to(counter, LEFT)
        self.add(counter, label_steps)

        # ==========================================
        # --- ITERATION 1: CỰC KỲ CHI TIẾT ---
        # ==========================================
        # Đã đổi tên tiêu đề theo yêu cầu
        step_title = Text(
            "Iteration 1: Step by Step", font_size=24, color=YELLOW
        ).to_edge(UP)
        self.play(Write(step_title))

        # Trích xuất và hiển thị giá trị hiện tại
        curr_h_line = DashedLine(
            start=axes.c2p(curr_x, curr_y), end=axes.c2p(0, curr_y), color=YELLOW
        )
        curr_text = MathTex(
            f"f(x_{{curr}}) \\approx {curr_y:.2f}", font_size=24, color=YELLOW
        )
        curr_text.next_to(curr_h_line, LEFT, buff=0.2)

        self.play(Create(curr_h_line), Write(curr_text))
        self.wait(1)

        # Chọn điểm láng giềng
        epsilon = 0.8
        next_x = curr_x + epsilon
        next_y = func(next_x)

        ghost_dot = Dot(axes.c2p(next_x, next_y), color=RED, radius=0.1)
        ghost_v_line = axes.get_vertical_line(ghost_dot.get_center(), color=RED)

        self.play(FadeIn(ghost_dot), Create(ghost_v_line))

        # Gióng giá trị láng giềng sang trục Y
        next_h_line = DashedLine(
            start=axes.c2p(next_x, next_y), end=axes.c2p(0, next_y), color=RED
        )
        next_text = MathTex(
            f"f(x_{{new}}) \\approx {next_y:.2f}", font_size=24, color=RED
        )
        next_text.next_to(next_h_line, LEFT, buff=0.2).shift(UP * 0.3)

        self.play(Create(next_h_line), Write(next_text))
        self.wait(1)

        # Đặt câu hỏi so sánh
        compare_text = MathTex(f"{next_y:.2f} > {curr_y:.2f}?", font_size=32)
        compare_text.to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(compare_text))
        self.wait(1)

        # Đưa ra quyết định và Di chuyển
        if next_y > curr_y:
            yes_text = Text(
                "Yes! Accept new state.", font_size=24, color=GREEN
            ).next_to(compare_text, RIGHT)
            self.play(Write(yes_text))
            self.wait(0.5)

            # Xóa các râu ria
            self.play(
                FadeOut(curr_h_line),
                FadeOut(curr_text),
                FadeOut(next_h_line),
                FadeOut(next_text),
                FadeOut(compare_text),
                FadeOut(yes_text),
                FadeOut(step_title),
            )

            # Trượt Tracker đến vị trí mới
            self.play(
                x_tracker.animate.set_value(next_x), run_time=1.5, rate_func=smooth
            )
            curr_x = next_x

        self.play(FadeOut(ghost_dot), FadeOut(ghost_v_line))
        counter.set_value(1)
        self.wait(1)

        # ==========================================
        # --- 1000 ITERATIONS: TĂNG TỐC DẦN ĐỀU ---
        # ==========================================
        fast_title = Text("Accelerating...", font_size=24).to_edge(UP)
        self.play(Write(fast_title))

        for i in range(2, 1001):
            step = np.random.uniform(-0.2, 0.2)
            temp_x = np.clip(curr_x + step, 0, 10)

            if func(temp_x) > func(curr_x):
                curr_x = temp_x

                # Tùy chỉnh nhịp độ (Pacing) để mượt mắt hơn
                if i <= 5:
                    current_speed = 0.5  # Chậm vừa
                elif i <= 20:
                    current_speed = 0.15  # Nhanh dần
                else:
                    current_speed = 0.03  # Tốc độ tối đa

                self.play(
                    x_tracker.animate.set_value(curr_x),
                    counter.animate.set_value(i),
                    run_time=current_speed,
                    rate_func=linear,
                )
            else:
                if i % 50 == 0:
                    counter.set_value(i)
                    self.wait(0.01)

        self.play(FadeOut(fast_title))
        end_text = Text("Stuck at Local Optimum!", color=RED, font_size=32).to_edge(
            DOWN
        )
        self.play(Write(end_text))
        self.wait(2)
