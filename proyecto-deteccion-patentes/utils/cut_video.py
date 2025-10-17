from moviepy.editor import VideoFileClip

# Exit: 2:43:14
# Cut a 2mins section of entree and exit videos

ENTREE_START = 20
ENTREE_END = 24

# Entree
entree_video = VideoFileClip('entree_2ms.mp4')
entree_cut_video = entree_video.subclip(ENTREE_START, ENTREE_END)
entree_cut_video.write_videofile('entree_4s.mp4', codec='libx264', audio_codec='aac')

# EXIT_START = (2 * 60 * 60) + (43 * 60) + 14
# EXIT_END = EXIT_START + 120

# # Exit
# exit_video = VideoFileClip('exit.mp4')
# exit_cut_video = exit_video.subclip(EXIT_START, EXIT_END)
# exit_cut_video.write_videofile('exit_2ms.mp4', codec='libx264', audio_codec='aac')