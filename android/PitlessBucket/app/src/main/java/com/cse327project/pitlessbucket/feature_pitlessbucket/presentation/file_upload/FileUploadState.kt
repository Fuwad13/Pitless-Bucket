package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.file_upload

import android.net.Uri
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.UploadResponse

data class FileUploadState(
    val selectedFileUri: Uri? = null,
    val isUploading: Boolean = false,
    val error: String? = null,
    val uploadResponse: UploadResponse? = null
)

