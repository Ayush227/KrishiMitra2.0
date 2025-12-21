from .shared import get_header, get_navbar

def render_admin(users, posts, user):
    # Generate Users Table Rows
    user_rows = ""
    for u in users:
        user_rows += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding:15px;">#{u[0]}</td>
            <td style="font-weight:bold; color:#198754;">{u[1]}</td>
            <td>{u[2]}</td>
            <td>
                <a href="/admin/delete_user/{u[0]}" onclick="return confirm('Delete this user?')" 
                   style="background:#dc3545; color:white; padding:5px 10px; border-radius:5px; font-size:0.8rem;">Delete</a>
            </td>
        </tr>
        """

    # Generate Posts Table Rows
    post_rows = ""
    for p in posts:
        post_rows += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding:15px;">{p[1]}</td>
            <td style="color:#555;">{p[2]}</td>
            <td style="font-size:0.8rem; color:#888;">{p[3]}</td>
            <td>
                <a href="/admin/delete_post/{p[0]}" onclick="return confirm('Delete this post?')" 
                   style="background:#dc3545; color:white; padding:5px 10px; border-radius:5px; font-size:0.8rem;">Delete</a>
            </td>
        </tr>
        """

    return f"""
    {get_header("Admin Panel")}
    {get_navbar(user=user)}
    
    <div class="container">
        <h2 style="color: #dc3545; margin-bottom: 30px; border-bottom: 2px solid #dc3545; padding-bottom: 10px;">
            <i class="fas fa-user-shield"></i> Admin Control Panel
        </h2>

        <div class="card" style="margin-bottom: 40px; text-align: left;">
            <h3 style="color:#333; margin-bottom: 20px;">Registered Users ({len(users)})</h3>
            <div style="overflow-x: auto;">
                <table style="width:100%; border-collapse: collapse;">
                    <tr style="background:#f8f9fa; text-align:left;">
                        <th style="padding:15px;">ID</th><th>Username</th><th>Email</th><th>Action</th>
                    </tr>
                    {user_rows if user_rows else '<tr><td colspan="4" style="padding:20px; text-align:center;">No users found.</td></tr>'}
                </table>
            </div>
        </div>

        <div class="card" style="text-align: left;">
            <h3 style="color:#333; margin-bottom: 20px;">Community Posts ({len(posts)})</h3>
            <div style="overflow-x: auto;">
                <table style="width:100%; border-collapse: collapse;">
                    <tr style="background:#f8f9fa; text-align:left;">
                        <th style="padding:15px;">User</th><th>Content</th><th>Date</th><th>Action</th>
                    </tr>
                    {post_rows if post_rows else '<tr><td colspan="4" style="padding:20px; text-align:center;">No posts found.</td></tr>'}
                </table>
            </div>
        </div>
    </div>
    </body></html>
    """