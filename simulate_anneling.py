from manim import *
import numpy as np


class SA(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES, distance=15)

        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-3, 6, 1],
            x_length=10,
            y_length=10,
            z_length=5,
        )

        def func(x, y):
            bowl = 0.1 * (x**2 + y**2)
            global_min = 2.0 * np.exp(-(x**2 + y**2))
            local_min = 1.0 * np.exp(-((x - 3) ** 2 + (y - 3) ** 2))
            return bowl - global_min - local_min

        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(40, 40),
        )
        surface.set_style(fill_opacity=0.5, stroke_width=0.5, stroke_color=BLUE_C)

        graph_group = VGroup(axes, surface)
        graph_group.shift(DOWN * 1.0)
        self.add(graph_group)

        start_x, start_y = 3.0, 3.0
        curr_x, curr_y = start_x, start_y
        curr_z = func(curr_x, curr_y)

        T = 1.5
        alpha = 0.95

        x_tracker = ValueTracker(curr_x)
        y_tracker = ValueTracker(curr_y)

        ball = Sphere(radius=0.2, color=YELLOW)
        ball.add_updater(
            lambda m: m.move_to(
                axes.c2p(
                    x_tracker.get_value(),
                    y_tracker.get_value(),
                    func(x_tracker.get_value(), y_tracker.get_value()),
                )
            )
        )
        self.add(ball)

        title = Text("Simulated Annealing 3D", font_size=32, color=YELLOW).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        iter_label = Text("Iter: ", font_size=24).to_corner(UR).shift(LEFT * 1.5)
        self.add_fixed_in_frame_mobjects(iter_label)

        temp_label = Text("Temp (T): ", font_size=24).next_to(
            iter_label, DOWN, aligned_edge=LEFT
        )
        self.add_fixed_in_frame_mobjects(temp_label)

        iter_val = Text("0", font_size=24).next_to(iter_label, RIGHT)
        temp_val = Text(f"{T:.2f}", font_size=24, color=RED).next_to(temp_label, RIGHT)
        self.add_fixed_in_frame_mobjects(iter_val, temp_val)
        self.wait(1)

        step_title = Text(
            "Iteration 1: Escaping Local Minimum", font_size=24, color=GREEN
        )
        step_title.next_to(title, DOWN, aligned_edge=LEFT).shift(DOWN * 0.2)

        next_x, next_y = 3.6, 3.6
        next_z = func(next_x, next_y)
        delta_e = next_z - curr_z

        calc_1 = MathTex(f"\\Delta E = {delta_e:.2f} > 0", font_size=28)
        calc_2 = MathTex(
            f"P_{{accept}} = e^{{-\\Delta E / T}} \\approx {np.exp(-delta_e / T):.2f}",
            font_size=28,
        )
        calc_1.next_to(step_title, DOWN, aligned_edge=LEFT, buff=0.3)
        calc_2.next_to(calc_1, DOWN, aligned_edge=LEFT, buff=0.2)

        self.add_fixed_in_frame_mobjects(step_title, calc_1, calc_2)

        self.play(Write(step_title))
        self.play(Write(calc_1), Write(calc_2))
        self.wait(2.5)

        self.play(FadeOut(calc_1), FadeOut(calc_2), FadeOut(step_title))

        self.play(
            x_tracker.animate.set_value(next_x),
            y_tracker.animate.set_value(next_y),
            run_time=1.5,
            rate_func=smooth,
        )
        curr_x, curr_y, curr_z = next_x, next_y, next_z
        T *= alpha

        self.remove(iter_val, temp_val)
        iter_val = Text("1", font_size=24).next_to(iter_label, RIGHT)
        color_ratio = min(max(T / 1.5, 0), 1)
        curr_color = interpolate_color(BLUE, RED, color_ratio)
        temp_val = Text(f"{T:.2f}", font_size=24, color=curr_color).next_to(
            temp_label, RIGHT
        )
        self.add_fixed_in_frame_mobjects(iter_val, temp_val)
        self.wait(0.5)

        fast_title = Text("Cooling down...", font_size=24, color=RED)
        fast_title.next_to(title, DOWN, aligned_edge=LEFT).shift(DOWN * 0.2)
        self.add_fixed_in_frame_mobjects(fast_title)
        self.play(Write(fast_title))

        for i in range(2, 251):
            step_x = np.random.uniform(-1.0, 1.0)
            step_y = np.random.uniform(-1.0, 1.0)

            temp_x = np.clip(curr_x + step_x, -5, 5)
            temp_y = np.clip(curr_y + step_y, -5, 5)
            temp_z = func(temp_x, temp_y)

            delta_energy = temp_z - curr_z

            accept = False
            if delta_energy < 0:
                accept = True
            else:
                p_accept = np.exp(-delta_energy / T)
                if np.random.rand() < p_accept:
                    accept = True

            self.remove(iter_val, temp_val)
            iter_val = Text(f"{i}", font_size=24).next_to(iter_label, RIGHT)
            color_ratio = min(max(T / 1.5, 0), 1)
            curr_color = interpolate_color(BLUE, RED, color_ratio)
            temp_val = Text(f"{T:.2f}", font_size=24, color=curr_color).next_to(
                temp_label, RIGHT
            )
            self.add_fixed_in_frame_mobjects(iter_val, temp_val)

            if accept:
                curr_x, curr_y, curr_z = temp_x, temp_y, temp_z
                speed = 0.5 if i <= 10 else 0.05

                self.play(
                    x_tracker.animate.set_value(curr_x),
                    y_tracker.animate.set_value(curr_y),
                    run_time=speed,
                    rate_func=linear,
                )
            else:
                if i % 3 == 0:
                    self.wait(1 / 30)

            T *= alpha

        self.play(FadeOut(fast_title))
        end_text = Text("Global Minimum Reached!", color=GREEN, font_size=32).to_corner(
            DOWN
        )
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text))

        self.wait(3)
