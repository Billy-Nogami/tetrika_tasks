def appearance(intervals):
    events = []

    # Обработка интервала урока
    lesson = intervals['lesson']
    events.append((lesson[0], 1, 'lesson'))
    events.append((lesson[1], -1, 'lesson'))

    # Обработка интервалов ученика
    pupil = intervals['pupil']
    for i in range(0, len(pupil), 2):
        events.append((pupil[i], 1, 'pupil'))
        events.append((pupil[i+1], -1, 'pupil'))

    # Обработка интервалов учителя
    tutor = intervals['tutor']
    for i in range(0, len(tutor), 2):
        events.append((tutor[i], 1, 'tutor'))
        events.append((tutor[i+1], -1, 'tutor'))

    # События
    events.sort(key=lambda x: (x[0], x[1]))

    # Cчётчики
    lesson_cnt = pupil_cnt = tutor_cnt = 0
    total_time = 0
    current_start = None

    # Обработка событий
    for time, delta, source in events:

        if source == 'lesson':
            lesson_cnt += delta
        elif source == 'pupil':
            pupil_cnt += delta
        elif source == 'tutor':
            tutor_cnt += delta

        # Проверяем активное состояние
        active_now = (lesson_cnt > 0) and (pupil_cnt > 0) and (tutor_cnt > 0)
        if active_now:
            if current_start is None:
                current_start = time
        else:
            if current_start is not None:
                total_time += time - current_start
                current_start = None
    return total_time
