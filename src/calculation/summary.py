from calculation.rays import RayBundle


class Summary:
    def __init__(self, rays: list[RayBundle], calculation_time: float):
        self.calculation_time = calculation_time

        self.n_steps = len(rays)

        sizes = [ray_bundle.origins.shape[0] for ray_bundle in rays]

        self.initial_count = sizes[0]
        self.max_rays = max(sizes)

        self.total_rays = sum(sizes)

    def message(self):
        return f"{self.initial_count} initial rays, {self.max_rays} peak, {self.total_rays} total rays, {self.n_steps} steps, {self.calculation_time:.3g}s"

