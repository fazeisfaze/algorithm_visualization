from manim import *
import numpy as np


def rastrigin(x, y):
    A = 10
    val = (
        A * 2 + (x**2 - A * np.cos(2 * np.pi * x)) + (y**2 - A * np.cos(2 * np.pi * y))
    )
    return val


class DESections(ThreeDScene):
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
            Text("Differential Evolution (DE)", font_size=28, color=YELLOW)
            .to_corner(UL)
            .shift(DOWN * 0.2)
        )
        iter_label = Text("Generation: ", font_size=24).to_corner(UR).shift(LEFT * 1.5)
        iter_val = Text("0", font_size=24).next_to(iter_label, RIGHT)
        self.add_fixed_in_frame_mobjects(title, iter_label, iter_val)

        pop_size = 15
        bounds = [-2, 2]
        F = 0.8
        CR = 0.9

        population = np.random.uniform(bounds[0], bounds[1], (pop_size, 2))

        def get_3d_point(x, y):
            return axes.c2p(x, y, rastrigin(x, y) / 8)

        dots = VGroup(
            *[
                Dot3D(point=get_3d_point(p[0], p[1]), color=RED, radius=0.08)
                for p in population
            ]
        )
        self.add(dots)
        self.wait(1)

        step_title = Text(
            "Gen 1: Evaluating 1 Target Vector (X)", font_size=20, color=GREEN
        )
        step_title.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(step_title)

        target_idx = 0
        X = population[target_idx]
        self.play(dots[target_idx].animate.set_color(YELLOW).scale(1.5))
        self.wait(0.5)

        idxs = [idx for idx in range(pop_size) if idx != target_idx]
        a_idx, b_idx, c_idx = np.random.choice(idxs, 3, replace=False)
        a, b, c = population[a_idx], population[b_idx], population[c_idx]

        self.play(
            dots[a_idx].animate.set_color(BLUE),
            dots[b_idx].animate.set_color(BLUE),
            dots[c_idx].animate.set_color(BLUE),
        )

        V = a + F * (b - c)
        V = np.clip(V, bounds[0], bounds[1])

        mut_tex = MathTex("V_{mutant} = a + F(b - c)", font_size=28).next_to(
            step_title, DOWN, aligned_edge=LEFT
        )
        self.add_fixed_in_frame_mobjects(mut_tex)
        self.play(Write(mut_tex))

        ghost_V = Dot3D(point=get_3d_point(V[0], V[1]), color=WHITE, radius=0.08)
        self.add(ghost_V)
        self.wait(1.5)

        U = np.copy(X)
        j_rand = np.random.randint(0, 2)
        for j in range(2):
            if np.random.rand() < CR or j == j_rand:
                U[j] = V[j]

        cross_tex = MathTex(
            "U_{trial} = Crossover(X, V_{mutant})", font_size=28
        ).next_to(mut_tex, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(cross_tex)
        self.play(Write(cross_tex))

        ghost_U = Dot3D(point=get_3d_point(U[0], U[1]), color=ORANGE, radius=0.1)
        self.add(ghost_U)
        self.wait(1.5)

        f_U = rastrigin(U[0], U[1])
        f_X = rastrigin(X[0], X[1])

        sign = "<" if f_U < f_X else ">"
        sel_tex = MathTex(
            f"f(U_{{trial}}) {sign} f(X) \\rightarrow ", font_size=28
        ).next_to(cross_tex, DOWN, aligned_edge=LEFT)
        res_tex = Text(
            "Accept U" if f_U < f_X else "Keep X",
            font_size=24,
            color=GREEN if f_U < f_X else RED,
        ).next_to(sel_tex, RIGHT)
        self.add_fixed_in_frame_mobjects(sel_tex, res_tex)

        self.play(Write(sel_tex), Write(res_tex))
        self.wait(2)

        self.play(
            FadeOut(step_title),
            FadeOut(mut_tex),
            FadeOut(cross_tex),
            FadeOut(sel_tex),
            FadeOut(res_tex),
            FadeOut(ghost_V),
            FadeOut(ghost_U),
        )

        self.play(
            dots[target_idx].animate.set_color(RED).scale(1 / 1.5),
            dots[a_idx].animate.set_color(RED),
            dots[b_idx].animate.set_color(RED),
            dots[c_idx].animate.set_color(RED),
        )

        new_population = np.copy(population)
        current_fitness = np.array([rastrigin(p[0], p[1]) for p in population])

        for i in range(pop_size):
            idxs = [idx for idx in range(pop_size) if idx != i]
            a_idx, b_idx, c_idx = np.random.choice(idxs, 3, replace=False)
            a, b, c = population[a_idx], population[b_idx], population[c_idx]

            V = a + F * (b - c)
            V = np.clip(V, bounds[0], bounds[1])

            U = np.copy(population[i])
            j_rand = np.random.randint(0, 2)
            for j in range(2):
                if np.random.rand() < CR or j == j_rand:
                    U[j] = V[j]

            if rastrigin(U[0], U[1]) < current_fitness[i]:
                new_population[i] = U

        anims = [
            dots[i].animate.move_to(
                get_3d_point(new_population[i, 0], new_population[i, 1])
            )
            for i in range(pop_size)
        ]
        self.play(*anims, run_time=1.5)
        population = new_population

        self.remove(iter_val)
        iter_val = Text("1", font_size=24).next_to(iter_label, RIGHT)
        self.add_fixed_in_frame_mobjects(iter_val)

        fast_title = Text(
            "Accelerating to 1000 Generations...", font_size=20, color=RED
        )
        fast_title.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(fast_title)
        self.play(Write(fast_title))

        self.begin_ambient_camera_rotation(rate=0.08)

        iterations = 1000
        for it in range(2, iterations + 1):
            new_population = np.copy(population)
            current_fitness = np.array([rastrigin(p[0], p[1]) for p in population])
            changed = False

            for i in range(pop_size):
                idxs = [idx for idx in range(pop_size) if idx != i]
                a_idx, b_idx, c_idx = np.random.choice(idxs, 3, replace=False)
                a, b, c = population[a_idx], population[b_idx], population[c_idx]

                V = a + F * (b - c)
                V = np.clip(V, bounds[0], bounds[1])

                U = np.copy(population[i])
                j_rand = np.random.randint(0, 2)
                for j in range(2):
                    if np.random.rand() < CR or j == j_rand:
                        U[j] = V[j]

                if rastrigin(U[0], U[1]) < current_fitness[i]:
                    new_population[i] = U
                    changed = True

            population = new_population

            self.remove(iter_val)
            iter_val = Text(f"{it}", font_size=24).next_to(iter_label, RIGHT)
            self.add_fixed_in_frame_mobjects(iter_val)

            if changed:
                if it < 20:
                    speed = 0.1
                elif it < 100:
                    speed = 0.05
                else:
                    speed = 0.02

                anims = [
                    dots[i].animate.move_to(
                        get_3d_point(population[i, 0], population[i, 1])
                    )
                    for i in range(pop_size)
                ]
                self.play(*anims, run_time=speed, rate_func=linear)
            else:
                if it % 50 == 0:
                    self.wait(1 / 30)

        self.play(FadeOut(fast_title))
        self.stop_ambient_camera_rotation()

        best_final_idx = np.argmin([rastrigin(p[0], p[1]) for p in population])
        best_pos_3d = get_3d_point(
            population[best_final_idx, 0], population[best_final_idx, 1]
        )

        self.move_camera(phi=45 * DEGREES, theta=45 * DEGREES, zoom=1.5, run_time=2)

        result_circle = (
            Circle(radius=0.2, color=PURE_GREEN)
            .rotate(PI / 2, axis=RIGHT)
            .move_to(best_pos_3d)
        )
        self.play(Create(result_circle), Flash(dots[best_final_idx]))

        end_text = Text("Global Optimum Found!", font_size=32, color=GREEN).to_corner(
            UP
        )
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text))

        self.wait(2)
