import streamlit as st

class Printer:
    def __init__(self, title: str = "Logs"):
        if "printer_items" not in st.session_state:
            st.session_state.printer_items = {}
        if "hide_done_ids" not in st.session_state:
            st.session_state.hide_done_ids = set()
        self.expander_title = title
        self.container = None  # Will be created inside expander on first flush

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
            content, _ = st.session_state.printer_items[item_id]
            st.session_state.printer_items[item_id] = (content, True)
        self.flush()

    def flush(self) -> None:
        with st.expander(self.expander_title, expanded=True):
            if self.container is None:
                self.container = st.container()
            self.container.empty()
            with self.container:
                for item_id, (content, is_done) in st.session_state.printer_items.items():
                    if is_done:
                        if item_id in st.session_state.hide_done_ids:
                            st.markdown(f"- {content}", unsafe_allow_html=True)
                        else:
                            st.markdown(f"✅ **{content}**", unsafe_allow_html=True)
                    else:
                        st.markdown(f"⏳ _{content}_", unsafe_allow_html=True)
