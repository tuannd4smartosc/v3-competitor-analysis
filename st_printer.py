import streamlit as st

# Printer class for Streamlit
class Printer:
    def __init__(self):
        if "printer_items" not in st.session_state:
            st.session_state.printer_items = {}
        if "hide_done_ids" not in st.session_state:
            st.session_state.hide_done_ids = set()
        self.container = st.empty()

    def end(self) -> None:
        pass

    def hide_done_checkmark(self, item_id: str) -> None:
        st.session_state.hide_done_ids.add(item_id)
        self.flush()

    def update_item(
        self, item_id: str, content: str, is_done: bool = False, hide_checkmark: bool = False
    ) -> None:
        st.session_state.printer_items[item_id] = (content, is_done)
        if hide_checkmark:
            st.session_state.hide_done_ids.add(item_id)
        self.flush()

    def mark_item_done(self, item_id: str) -> None:
        if item_id in st.session_state.printer_items:
            content = st.session_state.printer_items[item_id][0]
            st.session_state.printer_items[item_id] = (content, True)
        self.flush()

    def flush(self) -> None:
        renderables = []
        for item_id, (content, is_done) in st.session_state.printer_items.items():
            if is_done:
                prefix = "\n\n✅ " if item_id not in st.session_state.hide_done_ids else ""
                renderables.append(prefix + content)
            else:
                renderables.append(f"⏳ {content}")
        self.container.write("\n".join(renderables) if renderables else "No tasks yet.")