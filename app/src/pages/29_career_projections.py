import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Career Projections")

tab1, tab2, tab3 = st.tabs(["Education Timeline", "Co-op Timeline", "Full-time Work Timeline"])

with tab1:
    st.header("Education: Taking Your Skills to the Next Level")
    st.write("""
If you’re looking to enhance your expertise, here are some great options to consider:

- **PlusOne Program at Northeastern:** This accelerated program lets you earn both a bachelor’s and a master’s degree in just five years. It’s an efficient way to deepen your knowledge in a field you’re passionate about, especially if your co-op experiences point toward a specialized area like data science, engineering, or project management.  
- **Certifications:** Complement your degree with certifications that employers value. For example, certifications in Python, SQL, or Tableau are perfect if you’re leaning toward data-focused roles, while project management certifications (like Agile or PMP) can help if you’re thinking about leadership-oriented positions.  
- **Think Long-Term:** If you’re considering a master’s, use your time now to explore research or projects that align with the field. Look for graduate assistantships, as they’re great for building your academic and professional resume while funding your studies.  
""")
with tab2:
    st.header("Co-op: Building on What You’ve Already Done")
    st.write("""
Your two co-ops are proof of your ability to succeed in the real world, and you should leverage that momentum:

- **Deepen Your Expertise:** Apply for a co-op in a similar field to the ones you’ve already completed. This will showcase your dedication and make you stand out to future employers as someone with significant depth in their chosen area.  
- **Broaden Strategically:** If you’re curious about exploring a complementary role, now is the time. For example, if your past co-ops were in software development, you might consider a role in product management to diversify your experience while staying relevant.  
- **Why It Matters:** Employers love seeing a progression in skills and responsibilities. A strong co-op record signals focus and readiness for advanced roles, making you more competitive when applying for full-time positions.  
""")

with tab3:
    st.header("Full-time: Preparing for the Big Step")
    st.write("""
As you think about transitioning to a full-time role, here’s how to approach it:

- **Leverage Your Co-ops:** Start by targeting companies you’ve already worked with during your co-ops. They know your work ethic, and you already have connections there—this could make transitioning to a full-time role much smoother.  
- **Be Strategic with Applications:** Highlight specific accomplishments from your co-ops on your resume and tailor your applications to each company. Show how you’ve made an impact in your previous roles.  
- **Network, Network, Network:** Build relationships with alumni, former coworkers, and industry professionals. Schedule coffee chats to learn from their experiences and get advice on breaking into your desired field. Referrals can often lead to opportunities you might not find online.  
- **Start Early:** Begin your job search about 6-8 months before graduation. Use platforms like LinkedIn, Handshake, and Glassdoor, but remember, personal connections are often the best way to land interviews.  
""")