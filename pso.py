from manim import *
import numpy as np
import random


def rastrigin(x, y):
    A = 10
    val = (
        A * 2 + (x**2 - A * np.cos(2 * np.pi * x)) + (y**2 - A * np.cos(2 * np.pi * y))
    )
    return val


class PSOSections(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES, distance=11)

        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[0, 40, 10],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        surface = Surface(
            lambda u, v: axes.c2p(u, v, rastrigin(u, v) / 8),
            u_range=[-2.1, 2.1],
            v_range=[-2.1, 2.1],
            resolution=(30, 30),
            should_make_jagged=False,
            fill_opacity=0.3,
            stroke_width=0.8,
            stroke_color=WHITE,
        )
        surface.set_fill_by_value(
            axes=axes, colors=[(BLUE, 0), (GREEN, 15), (YELLOW, 30), (RED, 60)], axis=2
        )

        graph_group = VGroup(axes, surface).shift(DOWN * 0.5)
        self.add(graph_group)

        title = (
            Text("Particle Swarm Optimization (PSO)", font_size=28, color=YELLOW)
            .to_corner(UL)
            .shift(DOWN * 0.2)
        )
        iter_label = Text("Iteration: ", font_size=24).to_corner(UR).shift(LEFT * 1.5)
        iter_val = Text("0", font_size=24).next_to(iter_label, RIGHT)
        self.add_fixed_in_frame_mobjects(title, iter_label, iter_val)

        pop_size = 20
        bounds = [-2.0, 2.0]
        dim = 2
        w = 0.729
        c1 = 1.49445
        c2 = 1.49445

        positions = np.random.uniform(bounds[0], bounds[1], (pop_size, dim))
        velocities = np.random.uniform(-1, 1, (pop_size, dim))
        p_bests = np.copy(positions)
        p_best_scores = np.array([rastrigin(p[0], p[1]) for p in positions])

        g_best_idx = np.argmin(p_best_scores)
        g_best_score = p_best_scores[g_best_idx]
        g_best_pos = np.copy(positions[g_best_idx])

        def get_3d_point(x, y):
            return axes.c2p(x, y, rastrigin(x, y) / 8)

        dots = VGroup(
            *[
                Dot3D(point=get_3d_point(p[0], p[1]), color=RED, radius=0.08)
                for p in positions
            ]
        )
        self.add(dots)
        self.wait(1)

        step_title = Text(
            "Iter 1: Velocity & Position Update", font_size=20, color=GREEN
        )
        step_title.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(step_title)

        g_best_dot = Dot3D(
            point=get_3d_point(g_best_pos[0], g_best_pos[1]), color=YELLOW, radius=0.15
        )
        self.add(g_best_dot)
        self.play(Flash(g_best_dot, color=YELLOW))

        eq_1 = MathTex(
            "v(t+1) = w \\cdot v(t) + c_1 r_1 (P_{best} - x) + c_2 r_2 (G_{best} - x)",
            font_size=24,
        )
        eq_2 = MathTex("x(t+1) = x(t) + v(t+1)", font_size=24)
        eq_group = VGroup(eq_1, eq_2).arrange(DOWN, aligned_edge=LEFT)
        eq_group.next_to(step_title, DOWN, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(eq_group)
        self.play(Write(eq_group))
        self.wait(2.5)

        self.play(FadeOut(step_title), FadeOut(eq_group))

        for i in range(pop_size):
            r1 = np.random.rand(dim)
            r2 = np.random.rand(dim)
            velocities[i] = (
                (w * velocities[i])
                + (c1 * r1 * (p_bests[i] - positions[i]))
                + (c2 * r2 * (g_best_pos - positions[i]))
            )
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], bounds[0], bounds[1])

            fitness = rastrigin(positions[i, 0], positions[i, 1])
            if fitness < p_best_scores[i]:
                p_best_scores[i] = fitness
                p_bests[i] = np.copy(positions[i])
                if fitness < g_best_score:
                    g_best_score = fitness
                    g_best_pos = np.copy(positions[i])

        anims = [
            dots[i].animate.move_to(get_3d_point(positions[i, 0], positions[i, 1]))
            for i in range(pop_size)
        ]
        anims.append(
            g_best_dot.animate.move_to(get_3d_point(g_best_pos[0], g_best_pos[1]))
        )

        self.play(*anims, run_time=1.5, rate_func=smooth)

        self.remove(iter_val)
        iter_val = Text("1", font_size=24).next_to(iter_label, RIGHT)
        self.add_fixed_in_frame_mobjects(iter_val)

        iterations = 300
        fast_title = Text(
            f"Swarm converging... (Max {iterations} Iters)", font_size=20, color=RED
        )
        fast_title.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(fast_title)
        self.play(Write(fast_title))

        self.begin_ambient_camera_rotation(rate=0.08)

        for it in range(2, iterations + 1):
            changed = False

            for i in range(pop_size):
                r1 = np.random.rand(dim)
                r2 = np.random.rand(dim)
                velocities[i] = (
                    (w * velocities[i])
                    + (c1 * r1 * (p_bests[i] - positions[i]))
                    + (c2 * r2 * (g_best_pos - positions[i]))
                )
                positions[i] += velocities[i]
                positions[i] = np.clip(positions[i], bounds[0], bounds[1])

                if np.linalg.norm(velocities[i]) > 0.001:
                    changed = True

                fitness = rastrigin(positions[i, 0], positions[i, 1])
                if fitness < p_best_scores[i]:
                    p_best_scores[i] = fitness
                    p_bests[i] = np.copy(positions[i])
                    if fitness < g_best_score:
                        g_best_score = fitness
                        g_best_pos = np.copy(positions[i])

            self.remove(iter_val)
            iter_val = Text(f"{it}", font_size=24).next_to(iter_label, RIGHT)
            self.add_fixed_in_frame_mobjects(iter_val)

            if changed:
                speed = 0.1 if it < 30 else 0.03
                anims = [
                    dots[i].animate.move_to(
                        get_3d_point(positions[i, 0], positions[i, 1])
                    )
                    for i in range(pop_size)
                ]
                anims.append(
                    g_best_dot.animate.move_to(
                        get_3d_point(g_best_pos[0], g_best_pos[1])
                    )
                )
                self.play(*anims, run_time=speed, rate_func=linear)
            else:
                if it % 20 == 0:
                    self.wait(1 / 30)

        self.play(FadeOut(fast_title))
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=45 * DEGREES, theta=45 * DEGREES, zoom=1.5, run_time=2)

        result_circle = (
            Circle(radius=0.2, color=PURE_GREEN)
            .rotate(PI / 2, axis=RIGHT)
            .move_to(get_3d_point(g_best_pos[0], g_best_pos[1]))
        )
        self.play(Create(result_circle), Flash(g_best_dot, color=GREEN))

        end_text = Text("Global Optimum Found!", font_size=32, color=GREEN).to_corner(
            UP
        )
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text))

        self.wait(2)
