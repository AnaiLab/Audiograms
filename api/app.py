from flask import Flask, render_template, request
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI Agg backend
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract submitted data
        data = request.form
        frequencies = [250, 500, 1000, 2000, 4000, 8000]
        results = {
            'left_air': [int(data.get(f'left_air_{freq}', 0)) for freq in frequencies],
            'left_bone': [int(data.get(f'left_bone_{freq}', 0)) for freq in frequencies],
            'right_air': [int(data.get(f'right_air_{freq}', 0)) for freq in frequencies],
            'right_bone': [int(data.get(f'right_bone_{freq}', 0)) for freq in frequencies],
        }

        # Generate plot
        fig, ax = plt.subplots()
        ax.plot(frequencies, results['right_air'], marker='o', linestyle='-', color='red', label='Right Ear Air')
        ax.plot(frequencies, results['left_air'], marker='x', linestyle='-', color='blue', label='Left Ear Air')
        ax.plot(frequencies, results['right_bone'], marker='<', linestyle=':', color='red', label='Right Ear Bone')
        ax.plot(frequencies, results['left_bone'], marker='>', linestyle=':', color='blue', label='Left Ear Bone')

        ax.set_title('Audiogram')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Hearing Threshold (dB HL)')
        ax.set_ylim(120, -10)
        y_ticks = list(range(-10, 121, 10))
        ax.set_yticks(y_ticks)
        ax.set_xscale('log')
        ax.set_xticks(frequencies)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        # Convert plot to PNG image
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

        return render_template('index.html', plot_url=plot_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
