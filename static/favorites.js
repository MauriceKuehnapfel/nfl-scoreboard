const scrollKey = "favoriteScroll";

// Save the position when a favourite form is submitted.
document.querySelectorAll(".favorite-form").forEach((form) => {
	form.addEventListener("submit", () => {
		sessionStorage.setItem(
			scrollKey,
			JSON.stringify({
				path: window.location.pathname,
				week: form.elements.week.value,
				y: window.scrollY,
			}),
		);
	});
});

// Restore it after the page and fonts have loaded.
window.addEventListener("load", async () => {
	const saved = sessionStorage.getItem(scrollKey);

	if (!saved) return;

	sessionStorage.removeItem(scrollKey);

	const position = JSON.parse(saved);
	const currentWeek =
		new URLSearchParams(window.location.search).get("week") || "Week 1";

	if (
		position.path !== window.location.pathname ||
		position.week !== currentWeek
	) {
		return;
	}

	await document.fonts.ready;

	// Temporarily disable your CSS smooth scrolling.
	const root = document.documentElement;
	const previousBehavior = root.style.scrollBehavior;

	root.style.scrollBehavior = "auto";
	window.scrollTo(0, position.y);
	root.style.scrollBehavior = previousBehavior;
});
